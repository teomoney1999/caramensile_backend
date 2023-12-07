'''
    app: Flask(__name__)
            |   
            v
    bp: Blueprint(__name__)
            |
            v
    view: APIView
            |
            v
        Resource
            |
            v
        MethodView
            |
            v
          View
'''
from flask_restful import Resource
from flask import Response, request, make_response, jsonify
from werkzeug.exceptions import HTTPException
from ....database import db as default_db
from ..exception import *
from .helpers import *
from .search import (search)

from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

class ValidationError(Exception):
    """Raised when there is a problem deserializing a dictionary into an
    instance of a SQLAlchemy model.

    """
    pass

def extract_error_messages(exception):
    """Tries to extract a dictionary mapping field name to validation error
    messages from `exception`, which is a validation exception as provided in
    the ``validation_exceptions`` keyword argument in the constructor of this
    class.

    Since the type of the exception is provided by the user in the constructor
    of this class, we don't know for sure where the validation error messages
    live inside `exception`. Therefore this method simply attempts to access a
    few likely attributes and returns the first one it finds (or ``None`` if no
    error messages dictionary can be extracted).

    """
    # 'errors' comes from sqlalchemy_elixir_validations
    if hasattr(exception, 'errors'):
        return exception.errors
    # 'message' comes from savalidation
    if hasattr(exception, 'message'):
        # TODO this works only if there is one validation error
        try:
            left, right = str(exception).rsplit(':', 1)
            left_bracket = left.rindex('[')
            right_bracket = right.rindex(']')
        except ValueError as exc:
            #current_app.logger.exception(str(exc))
            # could not parse the string; we're not trying too hard here...
            return None
        msg = right[:right_bracket].strip(' "')
        fieldname = left[left_bracket + 1:].strip()
        return {fieldname: msg}
    return None

class ApiView(Resource): 
    db = None 
    session = None
    
    def __init__(self, model=None, collection_name=None, primary_key="id", db=None, *args, **kw): 
        super().__init__(*args, **kw) 
        self.model = model 
        self.collection_name = collection_name
        self.primary_key = primary_key
        
        if db is not None: 
            self.db = db    
        else: 
            self.db = default_db
    
        self.session = kw.get("session", None)
        if self.session is None: 
            try:
                self.session = getattr(self.db, "session")
            except: 
                raise Exception("There is no session in Database Object!")
        else: 
            # self.session is not None
            pass
        
                
        serializer = kw.get("serializer", None) 
        if serializer is None: 
            self.serializer = self._inst_to_dict
        else: 
            self.serializer = serializer 
            
        deserializer = kw.get("deserializer", None) 
        validation_exceptions = kw.get("validation_exceptions", None)
        if deserializer is None: 
            self.deserializer = self._dict_to_inst
            # self.validation_exceptions = tuple(list(validation_exceptions) or [ValidationError])
        else: 
            self.deserializer = deserializer
        
        # TODO study about decorate in flask, then apply to every api

    def _instid_to_dict(self, instid):
        """Returns the dictionary representation of the instance specified by
        `instid`.

        If no such instance of the model exists, this method aborts with a
        :http:statuscode:`404`.

        """
        # print("=====", type(instid), self.primary_key)
        inst = get_by(self.session, self.model, instid, self.primary_key)
        if inst is None:
            return make_response(jsonify(dict(message='No result found')), 520)
        return self._inst_to_dict(inst)
    
    def _inst_to_dict(self, inst):
        """Returns the dictionary representation of the specified instance.

        This method respects the include and exclude columns specified in the
        constructor of this class.

        """
        # create a placeholder for the relations of the returned models
        relations = frozenset(get_relations(self.model))
        # do not follow relations that will not be included in the response
        # if self.include_columns is not None:
        #     cols = frozenset(self.include_columns)
        #     rels = frozenset(self.include_relations)
        #     relations &= (cols | rels)
        # elif self.exclude_columns is not None:
        #     relations -= frozenset(self.exclude_columns)
        deep = dict((r, {}) for r in relations)        
        return to_dict(inst, deep, 
                    #    exclude=self.exclude_columns,
                    #    exclude_relations=self.exclude_relations,
                    #    include=self.include_columns,
                    #    include_relations=self.include_relations,
                    #    include_methods=self.include_methods
                       )
    
    def _dict_to_inst(self, data):
        """Returns an instance of the model with the specified attributes."""
        # Check for any request parameter naming a column which does not exist
        # on the current model.
        for field in data:
            if not has_field(self.model, field):
                msg = "Model does not have field '{0}'".format(field)
                raise ValidationError(msg)

        # Getting the list of relations that will be added later
        cols = get_columns(self.model)
        relations = get_relations(self.model)

        # Looking for what we're going to set on the model right now
        colkeys = cols.keys()
        paramkeys = data.keys()
        props = set(colkeys).intersection(paramkeys).difference(relations)

        # Special case: if there are any dates, convert the string form of the
        # date into an instance of the Python ``datetime`` object.
        data = strings_to_dates(self.model, data)

        # Instantiate the model with the parameters.
        modelargs = dict([(i, data[i]) for i in props])
        instance = self.model(**modelargs)

        # Handling relations, a single level is allowed
        for col in set(relations).intersection(paramkeys):
            submodel = get_related_model(self.model, col)

            if type(data[col]) == list:
                # model has several related objects
                for subparams in data[col]:
                    subinst = get_or_create(self.session, submodel,
                                            subparams)
                    try:
                        getattr(instance, col).append(subinst)
                    except AttributeError:
                        attribute = getattr(instance, col)
                        attribute[subinst.key] = subinst.value
            else:
                # model has single related object
                if data[col] is not None:
                    subinst = get_or_create(self.session, submodel, data[col])
                    setattr(instance, col, subinst)
        return instance
    
    def _handle_validation_exception(self, exception):
        """Rolls back the session, extracts validation error messages, and
        returns a :func:`flask.jsonify` response with :http:statuscode:`400`
        containing the extracted validation error messages.

        Again, *this method calls
        :meth:`sqlalchemy.orm.session.Session.rollback`*.

        """
        self.session.rollback()
        errors = extract_error_messages(exception) or \
            'Could not determine specific validation errors'
        return make_response(jsonify(dict(validation_errors=errors)), 520)
    
     # TODO change this to have more sensible arguments
    def _update_relations(self, query, params):
        """Adds, removes, or sets models which are related to the model
        specified in the constructor of this class.

        This function does not commit the changes made to the database. The
        calling function has that responsibility.

        This method returns a :class:`frozenset` of strings representing the
        names of relations which were modified.

        `query` is a SQLAlchemy query instance that evaluates to all instances
        of the model specified in the constructor of this class that should be
        updated.

        `params` is a dictionary containing a mapping from name of the relation
        to modify (as a string) to either a list or another dictionary. In the
        former case, the relation will be assigned the instances specified by
        the elements of the list, which are dictionaries as described below.
        In the latter case, the inner dictionary contains at most two mappings,
        one with the key ``'add'`` and one with the key ``'remove'``. Each of
        these is a mapping to a list of dictionaries which represent the
        attributes of the object to add to or remove from the relation.

        If one of the dictionaries specified in ``add`` or ``remove`` (or the
        list to be assigned) includes an ``id`` key, the object with that
        ``id`` will be attempt to be added or removed. Otherwise, an existing
        object with the specified attribute values will be attempted to be
        added or removed. If adding, a new object will be created if a matching
        object could not be found in the database.

        If a dictionary in one of the ``'remove'`` lists contains a mapping
        from ``'__delete__'`` to ``True``, then the removed object will be
        deleted after being removed from each instance of the model in the
        specified query.

        """
        relations = get_relations(self.model)
        tochange = frozenset(relations) & frozenset(params)

        for columnname in tochange:
            # Check if 'add' or 'remove' is being used
            if (isinstance(params[columnname], dict)
                and any(k in params[columnname] for k in ['add', 'remove'])):

                toadd = params[columnname].get('add', [])
                toremove = params[columnname].get('remove', [])
                self._add_to_relation(query, columnname, toadd=toadd)
                self._remove_from_relation(query, columnname,
                                           toremove=toremove)
            else:
                toset = params[columnname]
                self._set_on_relation(query, columnname, toset=toset)
        return tochange
    
    def _set_on_relation(self, query, relationname, toset=None):
        """Sets the value of the relation specified by `relationname` on each
        instance specified by `query` to have the new or existing related
        models specified by `toset`.

        This function does not commit the changes made to the database. The
        calling function has that responsibility.

        `query` is a SQLAlchemy query instance that evaluates to all instances
        of the model specified in the constructor of this class that should be
        updated.

        `relationname` is the name of a one-to-many relationship which exists
        on each model specified in `query`.

        `toset` is either a dictionary or a list of dictionaries, each
        representing the attributes of an existing or new related model to
        set. If a dictionary contains the key ``'id'``, that instance of the
        related model will be added. Otherwise, the
        :func:`helpers.get_or_create` method will be used to get or create a
        model to set.

        """
        submodel = get_related_model(self.model, relationname)
        if isinstance(toset, list):
            value = [get_or_create(self.session, submodel, d) for d in toset]
        else:
            value = get_or_create(self.session, submodel, toset)
        for instance in query:
            setattr(instance, relationname, value)
    
    def _add_to_relation(self, query, relationname, toadd=None):
        """Adds a new or existing related model to each model specified by
        `query`.

        This function does not commit the changes made to the database. The
        calling function has that responsibility.

        `query` is a SQLAlchemy query instance that evaluates to all instances
        of the model specified in the constructor of this class that should be
        updated.

        `relationname` is the name of a one-to-many relationship which exists
        on each model specified in `query`.

        `toadd` is a list of dictionaries, each representing the attributes of
        an existing or new related model to add. If a dictionary contains the
        key ``'id'``, that instance of the related model will be
        added. Otherwise, the :func:`helpers.get_or_create` class method will
        be used to get or create a model to add.

        """
        submodel = get_related_model(self.model, relationname)
        if isinstance(toadd, dict):
            toadd = [toadd]
        for dictionary in toadd or []:
            subinst = get_or_create(self.session, submodel, dictionary)
            try:
                for instance in query:
                    getattr(instance, relationname).append(subinst)
            except AttributeError as exception:
                #current_app.logger.exception(str(exception))
                setattr(instance, relationname, subinst)

    def _remove_from_relation(self, query, relationname, toremove=None):
        """Removes a related model from each model specified by `query`.

        This function does not commit the changes made to the database. The
        calling function has that responsibility.

        `query` is a SQLAlchemy query instance that evaluates to all instances
        of the model specified in the constructor of this class that should be
        updated.

        `relationname` is the name of a one-to-many relationship which exists
        on each model specified in `query`.

        `toremove` is a list of dictionaries, each representing the attributes
        of an existing model to remove. If a dictionary contains the key
        ``'id'``, that instance of the related model will be
        removed. Otherwise, the instance to remove will be retrieved using the
        other attributes specified in the dictionary. If multiple instances
        match the specified attributes, only the first instance will be
        removed.

        If one of the dictionaries contains a mapping from ``'__delete__'`` to
        ``True``, then the removed object will be deleted after being removed
        from each instance of the model in the specified query.

        """
        submodel = get_related_model(self.model, relationname)
        for dictionary in toremove or []:
            remove = dictionary.pop('__delete__', False)
            if 'id' in dictionary:
                subinst = get_by(self.session, submodel, dictionary['id'])
            else:
                subinst = self.query(submodel).filter_by(**dictionary).first()
            for instance in query:
                getattr(instance, relationname).remove(subinst)
            if remove:
                self.session.delete(subinst)
    
    
    

class CollectionApiView(ApiView): 
    def __init__(self, model=None, collection_name=None, primary_key="id", db=None, *args, **kw): 
        super(CollectionApiView, self).__init__(model, collection_name, primary_key, db, *args, **kw) 
    
    
    def get(self, *args, **kwargs): 
        # GET MANY
        try: 
            # TODO add search_params 
            result = search(self.session, self.model, {})
        except NoResultFound: 
            return make_response(jsonify(dict(message='No result found')), 520)
        except Exception as exception: 
            return make_response(jsonify(dict(message='Unable to construct query')), 520)
        
        # create a placeholder for the relations of the returned models
        relations = frozenset(get_relations(self.model))
        deep = dict((r, {}) for r in relations)
        
        # for security purposes, don't transmit list as top-level JSON
        if isinstance(result, Query): 
            # TODO using _paginated()
            objects = [to_dict(r, deep) for r in result]
            result = dict(page=1, objects=objects, total_page=1, num_results=len(objects))
            pass
        else: 
            result = to_dict(result, deep) 
            
        return make_response(jsonify(result), 200)
 
    def post(self): 
        try:
            data = request.json or {}
        except (InternalServerError, TypeError, ValueError, OverflowError) as exception: 
            return make_response(jsonify(message='Unable to decode data'), 520)
        
        # for field in data: 
        #     if not has_field(self.model, field): 
        #         msg = "Model does not have field '{0}'".format(field)
        #         return  make_response(jsonify(message=msg), 520)
        
        try: 
            instance = self.deserializer(data) 
            self.session.add(instance) 
            self.session.commit()
            # Get the dictionary representation of the new instance as it
            # appears in the database.
            result = self.serializer(instance)
        except Exception as exception:
            return self._handle_validation_exception(exception)
        
        # Get primary key
        # pk_name = self.primary_key or primary_key_name(self.model)
        
        # The URL at which a client can access the newly created instance
        # of the model.
        # primary_key = str(result[pk_name])
        # url = '{0}/{1}'.format(request.url, primary_key)
        # Provide that URL in the Location header in the response.
        # headers = dict(Location=url) 
        
        return make_response(jsonify(to_dict(result)), 201)
        
    
class InstanceApiView(ApiView): 
    def __init__(self, model=None, collection_name=None, primary_key="id", db=None, *args, **kw): 
        super(InstanceApiView, self).__init__(model, collection_name, primary_key, db, *args, **kw) 
    
    def get(self, id=None): 
        # GET SINGLE
        instance = get_by(self.session, self.model, id)      
        if instance is None: 
            return make_response(jsonify(message='No result found!'), 520)
        
        result = self.serializer(instance)
        # TODO set headers
        return make_response(jsonify(result), 200)
         
    
    def put(self, id=None): 
        instance = get_by(self.session, self.model, id) 
        if instance is None: 
            return make_response(jsonify(message='No result found!'), 520)

        try:
            data = request.json or {}
        except (InternalServerError, TypeError, ValueError, OverflowError) as exception: 
            return make_response(jsonify(message='Unable to decode data'), 520)
        
        for field in data: 
            if not has_field(self.model, field): 
                msg = "Model does not have field '{0}'".format(field)
                return  make_response(jsonify(message=msg), 520)
        
        query = query_by_primary_key(self.session, self.model, id)
        if query.count() == 0: 
            return make_response(jsonify(message='No result found!'), 520)
        assert query.count() == 1, 'Multiple rows with same ID' # for debug only
        
        # Relations handling
        try: 
            relations = self._update_relations(query, data)
        except ValidationError as exception: 
            return self._handle_validation_exception(exception)
        
        field_list = frozenset(data) ^ relations 
        
        data = dict((field, data[field]) for field in field_list)
        
        try:
            # Let's update all instances present in the query
            num_modified = 0
            if data:
                for item in query.all():
                    for field, value in data.items():
                        setattr(item, field, value)
                    num_modified += 1
            self.session.commit()
        except ValidationError as exception:
            #current_app.logger.exception(str(exception))
            return self._handle_validation_exception(exception)
 
        result = self._instid_to_dict(id)
        
        return make_response(jsonify(to_dict(result)), 200)
        
    
    def delete(self, id=None): 
        # Flag to ensure that instance have been deleted
        was_deleted = False
        instance = get_by(self.session, self.model, id) 
        
        if instance is None: 
            return make_response(jsonify(message='No result found!'), 520)
        
        self.session.delete(instance) 
        was_deleted = len(self.session.deleted) > 0
        self.session.commit()
        
        return make_response(jsonify({}), 200) if was_deleted else make_response(jsonify({}), 520)
        

    
    