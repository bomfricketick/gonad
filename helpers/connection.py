import pyodbc
import os
import json
from profile import read_profile
from contextlib import contextmanager

def keys_exists(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keys_exists() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keys_exists() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

def get_credentials_from_profile():
    """Read profile and return credentials"""
    profile = read_profile(profiles_dir="./")
    if not keys_exists(profile, 'project'):
        return('the root key "project" is missing from profiles.yml')
    if not keys_exists(profile, 'project', 'target'):
        return('the key "target" is missing from profiles.yml')
    if not keys_exists(profile, 'project', 'outputs'):
        return('the key "outputs" is missing from profiles.yml')
    target = profile['project']['target']
    outputs = profile['project']['outputs'].get(target)
    if not outputs:
        print('the target is not found in profiles.yml')
        return None
    else:
        return outputs


def switch(key):
    return {
        'driver': 'DRIVER',
        'server': 'SERVER',
        'port': 'Port',
        'database': 'Database',
        'schema': 'Schema',
        'user': 'UID',
        'password': 'PWD',
        'trust_cert': 'TrustServerCertificate'
    }.get(key, key)


def bool_to_connection_string_arg(key: str, value: bool) -> str:
    """
    Convert a boolean to a connection string argument.
    Parameters
    ----------
    key : str
        The key to use in the connection string.
    value : bool
        The boolean to convert.
    Returns
    -------
    out : str
        The connection string argument.
    """
    return f'{switch(key)}={"Yes" if value else "No"}'




def create_connection_string(credentials: dict):
    # print(credentials)
    if not credentials:
        return None
    else:
        # target_name = get_target()
        # credentials = get_outputs()
        con_str = [f"DRIVER={{{credentials.get('driver')}}}"]

        server = credentials.get('server')
        if "\\" in server:
            # If there is a backslash \ in the host name, the host is a
            # SQL Server named instance. In this case then port number has to be omitted.
            con_str.append(f"SERVER={credentials.get('server')}")
        else:
            con_str.append(f"SERVER={credentials.get('server')},{credentials.get('port')}")

        con_str.append(f"Database={credentials.get('database')}")

        assert credentials.get('authentication') is not None

        if "ActiveDirectory" in credentials.get('authentication'):
            con_str.append(f"Authentication={credentials.get('authentication')}")

            if credentials.get('authentication') == "ActiveDirectoryPassword":
                con_str.append(f"UID={{{credentials.get('user')}}}")
                con_str.append(f"PWD={{{credentials.get('password')}}}")
            elif credentials.get('authentication') == "ActiveDirectoryInteractive":
                con_str.append(f"UID={{{credentials.get('user')}}}")

        elif credentials.get('windows_login'):
            con_str.append("trusted_connection=Yes")
        elif credentials.get('authentication') == "sql":
            con_str.append(f"UID={credentials.get('user')}")
            con_str.append(f"PWD={credentials.get('password')}")

        # https://docs.microsoft.com/en-us/sql/relational-databases/native-client/features/using-encryption-without-validation?view=sql-server-ver15
        assert credentials.get('encrypt') is not None
        assert credentials.get('trust_cert') is not None

        con_str.append(bool_to_connection_string_arg("encrypt", credentials.get('encrypt')))
        con_str.append(
            bool_to_connection_string_arg("TrustServerCertificate", credentials.get('trust_cert'))
        )

        # plugin_version = __version__.version
        application_name = f"gonad-{credentials.get('type')}"
        con_str.append(f"Application Name={application_name}")

        con_str_concat = ";".join(con_str)

        index = []
        for i, elem in enumerate(con_str):
            if "password=" in elem.lower():
                index.append(i)

        if len(index) != 0:
            con_str[index[0]] = "PWD=***"

        con_str_display = ";".join(con_str)


        # print(con_str)
        # print(con_str_concat)
        # print(con_str_display)
        return con_str_concat


print(create_connection_string(get_credentials_from_profile()))

@contextmanager
def open_db(connection_str: str, autocommit: bool = True):
    connection = pyodbc.connect(connection_str)
    try:
        cursor = connection.cursor()
        yield cursor
    except pyodbc.DatabaseError as error:
        print('error')
    finally:
        connection.commit()
        connection.close()


def runSQL(con_str: str, sql: str):
    with open_db(connection_str=con_str, autocommit=True) as cursor:
        cursor.execute(sql)
        query_results = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        return query_results


# test = runSQL(con_str=create_connection_string(get_credentials_from_profile()), sql="SELECT * FROM INFORMATION_SCHEMA.TABLES")
# print(test)