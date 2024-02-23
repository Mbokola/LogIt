#!/usr/bin/python3

from log import Log

create_a_log = Log()
log_name = 'Test_Log2'
fields = ['col4', 'col5', 'col6']
create_a_log.create_log(log_name, fields)
print(create_a_log.get_log_field('Test_Log'))
create_a_log.make_log_entry('Test_Log', {'col1': 'Col1 third entry',
                                         'col2': 'Col2 third entry',
                                         'col3': 'Col3 third entry'
                                         })
