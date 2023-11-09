import jinja2

from email_notification_service.utils.config import Config


class TemplateManager:
    def __init__(self):
        self._conf = Config()
        self._template_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader([self._conf.TEMPLATE_DIR])
        )

    def render_template(self, file_name: str, **kwargs):
        """
        Render Jinja2 template from file

        Args:
            file_name (str) - File name of the template to be rendered
        """

        template = self._template_env.get_template(file_name)
        return template.render(**kwargs)
