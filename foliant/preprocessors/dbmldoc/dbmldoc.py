'''
Preprocessor for Foliant documentation authoring tool.
Generates documentation from dbml.
'''

import os
from pydbml import PyDBML
from pathlib import Path, PosixPath
from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
from distutils.dir_util import remove_tree
from shutil import copyfile
from jinja2 import Environment, FileSystemLoader
from pkg_resources import resource_filename

from foliant.preprocessors.utils.preprocessor_ext import (BasePreprocessorExt,
                                                          allow_fail)
from foliant.preprocessors.utils.combined_options import (Options,
                                                          CombinedOptions,
                                                          validate_exists,
                                                          rel_path_convertor)


class Preprocessor(BasePreprocessorExt):
    tags = ('dbmldoc',)

    defaults = {
        'spec_url': [],
        'spec_path': '',
        'doc': True,
        'scheme': True,
        'template': 'dbml.j2',
        'scheme_template': 'scheme.j2'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('dbmldoc')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')

        # '/' for abspaths
        self._env = \
            Environment(loader=FileSystemLoader([str(self.project_path), '/']),
                        extensions=["jinja2.ext.do"])

        self._dbml_tmp = self.project_path / '.dbmlcache/'
        if self._dbml_tmp.exists():
            remove_tree(self._dbml_tmp)
        os.makedirs(self._dbml_tmp)

        self.options = Options(self.options,
                               validators={'spec_path': validate_exists})

    def _gather_specs(self,
                      urls: list,
                      path_: str or PosixPath or None) -> PosixPath:
        """
        Download first dbml spec from the url list; copy it into the
        temp dir and return path to it. If all urls fail — check path_ and
        return it.

        Return None if everything fails
        """
        self.logger.debug(f'Gathering specs. Got list of urls: {urls}, path: {path_}')
        if urls:
            for url in urls:
                try:
                    filename = self._dbml_tmp / f'dbml_spec'
                    urlretrieve(url, filename)
                    self.logger.debug(f'Using spec from {url} ({filename})')
                    return filename
                except (HTTPError, URLError) as e:
                    self._warning(f'\nCannot retrieve dbml spec file from url {url}. Skipping.',
                                  error=e)

        if path_:
            dest = self._dbml_tmp / f'dbml_spec'
            if not Path(path_).exists():
                self._warning(f"Can't find file {path_}. Skipping.")
            else:  # file exists
                copyfile(str(path_), str(dest))
                return dest

    def _process_jinja(self,
                       spec: PosixPath,
                       options: CombinedOptions) -> str:
        """Process dbml spec with jinja and return the resulting string"""
        data = PyDBML(spec)
        result = ''

        if options['doc']:
            if options.is_default('template') and not Path(options['template']).exists():
                # copy default template to project dir if it's doesn't exist there
                copyfile(
                    resource_filename(
                        __name__, 'template/' +
                        self.defaults['template']
                    ),
                    options['template']
                )
            try:
                template = self._env.get_template(str(options['template']))
                result += template.render(data=data)
            except Exception as e:
                self._warning(f'\nFailed to render doc template {options["template"]}',
                              error=e)
                return result

        if options['scheme']:
            if options.is_default('scheme_template') and\
                    not Path(options['scheme_template']).exists():
                # copy default template to project dir if it's doesn't exist there
                copyfile(
                    resource_filename(
                        __name__, 'template/' +
                        self.defaults['scheme_template']
                    ),
                    options['scheme_template']
                )
            try:
                template = self._env.get_template(str(options['scheme_template']))
                result += template.render(data=data)
            except Exception as e:
                self._warning(f'\nFailed to render scheme template {options["scheme_template"]}',
                              error=e)
                return result

        return result

    @allow_fail()
    def process_dbmldoc_blocks(self, block) -> str:
        tag_options = Options(self.get_options(block.group('options')),
                              convertors={'spec_path': rel_path_convertor(self.current_filepath.parent)})
        options = CombinedOptions(options={'config': self.options,
                                           'tag': tag_options},
                                  priority='tag',
                                  required=[('spec_url',),
                                            ('spec_path',)],
                                  defaults=self.defaults)
        self.logger.debug(f'Processing dbmldoc tag in {self.current_filepath}')
        spec_urls = options['spec_url']
        if spec_urls and isinstance(spec_urls, str):
            spec_urls = [spec_urls]
        spec_path = options['spec_path']
        spec = self._gather_specs(spec_urls, spec_path)
        if not spec:
            raise RuntimeError("No valid dbml spec file specified")

        return self._process_jinja(spec, options)

    def apply(self):
        self._process_tags_for_all_files(func=self.process_dbmldoc_blocks)
        self.logger.info('Preprocessor applied')
