<%!
    def parse_dict(data, indent=0):
        line = ''
        for key, value in data.items():
            if isinstance(value, dict):
                line += '  ' * indent + key + '\n'
                line += parse_dict(value, indent + 1)
            else:
                if isinstance(value, list): value = ' '.join(map(str, value))
                line += '  ' * indent + key + ' ' + value + '\n'
        return line
%>${parse_dict(data)}
