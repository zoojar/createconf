"""TestMain"""
import tempfile
import os
import argparse
from createconf.createconf import createconf

class TestMain:
    # pylint: disable=too-few-public-methods
    """
    Test the main function in the createconf module.
    """

    def test_main(self):
        """
        Test the main function with a given data, defaults, and a template file.
        It should create an output file with the merged data and template content.
        """
        data = '{"key1": "value1", "key2": "value2"}'
        defaults = '{"key1": "default_value1", "key2": "default_value2", "key3": "default_value3"}'
        ignore = []

        content = "key1: ${data['key1']}\nkey2: ${data['key2']}\nkey3: ${data.get('key3', '')}\n"

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as template_file:
            template_file.write(content)
            template_file_name = template_file.name
            template_file.close()

        with tempfile.NamedTemporaryFile(mode="w", delete=False) as outfile:
            outfile_name = outfile.name
            outfile.close()

            args = argparse.Namespace(
                data=data,
                defaults=defaults,
                template=template_file_name,
                ignore_keys=ignore,
                outfile=outfile_name,
                verbose=False,
                ignore_duplicate_keys=False,
            )

            try:
                createconf(args)
                with open(outfile_name, "r", encoding='utf-8') as ofile:
                    output = ofile.read()
                # Perform assertions
                assert "key1: value1" in output
                assert "key2: value2" in output
                assert "key3: default_value3" in output
            finally:
                os.unlink(outfile_name)
                os.unlink(template_file_name)
