"""Kaboom entry point and configuration."""
import websauna.system


class Initializer(websauna.system.Initializer):
    """An initialization configuration used for starting Kaboom.

    Override parent class methods to customize application behavior.
    """

    def configure_static(self):
        """Configure static asset serving and cache busting."""
        super(Initializer, self).configure_static()

        self.config.registry.static_asset_policy.add_static_view('my.app-static', 'my.app:static')

    def configure_templates(self):
        """Include our package templates folder in Jinja 2 configuration."""
        super(Initializer, self).configure_templates()

        self.config.add_jinja2_search_path('my.app:templates', name='.html', prepend=True)  # HTML templates for pages
        self.config.add_jinja2_search_path('my.app:templates', name='.txt', prepend=True)  # Plain text email templates (if any)
        self.config.add_jinja2_search_path('my.app:templates', name='.xml', prepend=True)  # Sitemap and misc XML files (if any)

    def configure_views(self):
        """Configure views for your application.

        Let the config scanner to pick ``@simple_route`` definitions from scanned modules. Alternative you can call ``config.add_route()`` and ``config.add_view()`` here.
        """
        # We override this method, so that we route home to our home screen, not Websauna default one
        from . import views
        self.config.scan(views)

    def configure_models(self):
        """Register the models of this application."""
        from . import models
        self.config.scan(models)

    def configure_model_admins(self):
        """Register the models of this application."""
        # Call parent which registers user and group admins
        super(Initializer, self).configure_model_admins()

        # Scan our admins
        from . import admins
        self.config.scan(admins)

    def include_addons(self):
        """Include a Websauna add on."""
        # i.e: To include websauna.newsletter, simply uncomment the following line.
        # self.config.include('websauna.newsletter')
        pass

    def run(self):
        super(Initializer, self).run()


def main(global_config, **settings):
    init = Initializer(global_config)
    init.run()
    return init.make_wsgi_app()
