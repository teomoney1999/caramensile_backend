from flask import Blueprint as BP
import typing as t

class Blueprint(BP): 
    def __init__(self, name: str,
        import_name: str,
        static_folder: t.Optional[t.Union[str, os.PathLike]] = None,
        static_url_path: t.Optional[str] = None,
        template_folder: t.Optional[t.Union[str, os.PathLike]] = None,
        url_prefix: t.Optional[str] = None,
        subdomain: t.Optional[str] = None,
        url_defaults: t.Optional[dict] = None,
        root_path: t.Optional[str] = None,
        # cli_group: t.Optional[str] = _sentinel,  # type: ignore): 
    ):
        super().__init__(
            import_name=import_name,
            static_folder=static_folder,
            static_url_path=static_url_path,
            template_folder=template_folder,
            root_path=root_path,
            url_prefix=url_prefix, 
            url_defaults=url_defaults, 
            subdomain=subdomain
        )
    
    def add_route(self)
        