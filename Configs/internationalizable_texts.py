from Configs.UserActions import userActions_list

mk = '@intl: '


class Texts:
    """ all texts for internationalization purposes TODO: internationalize """

    current_language = 'English'
    available_languages = ['English', 'pt-br']

    def __init__(self, language='default'):
        if language in self.available_languages:
            self.current_language = language

    def put(self, message_id, extra=1):
        if message_id is None:
            return ''

        if self.current_language == 'English':
            if message_id == 'COMMAND':
                actions = userActions_list
                return actions[extra]
            if message_id == 'MOVE':
                return mk + 'Recording movement: to the left, right or same-place chosen.'
            if message_id == 'TRASH':
                return mk + 'Backup will be done (retrievable trash can like). ' \
                            'Simple deletion or duplication found marker.'
            if message_id == 'GROUP':
                return mk + 'New grouping or ranking axis to be entered.'
            if message_id == 'QUIT':
                return mk + 'Quitting…'
            if message_id == 'IERROR':
                return mk + 'Input error. Possible answers:'
            if message_id == 'WERROR':
                return mk + 'Weird error found: [code '

        if self.current_language == 'pt-br':
            if message_id == 'COMMAND':
                actions = ['ERRO', '<-  ', '+>  ', '<=> ', 'APAGAR', 'DUPLICADO', 'AGRUPAR', 'SAIR']
                return actions[extra]
            if message_id == 'MOVE':
                return 'Movimentação gravada.'
            if message_id == 'TRASH':
                return 'Jogando na lixeira.'
            if message_id == 'GROUP':
                return 'Agrupando.'
            if message_id == 'QUIT':
                return 'Saindo…'
            if message_id == 'IERROR':
                return 'Erro: comando desconhecido. Os comandos são: '
            if message_id == 'WERROR':
                return 'Erro muito fora do normal: [código '
