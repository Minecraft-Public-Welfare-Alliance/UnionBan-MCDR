import time
from threading import Thread
from mcdreforged.api.all import *
import pymysql

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def close(self):
        self.connection.close()
    
    def get_rows(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM UnionBan")
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    
    def get_data(self, row):
        cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM UnionBan LIMIT %s, 1", (row,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def add_row(self, ID, IP, Reason, Reason_Text, isOnline, _from):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO UnionBan (ID, IP, Reason, Reason_Text, isOnline, `From`) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (ID, IP, Reason, Reason_Text, isOnline, _from))
        self.connection.commit()
        cursor.close()


def check_and_ban_players(server, config):
    db = MySQLDatabase(
        host=config['mysql_host'],
        user=config['mysql_user'],
        password=config['mysql_password'],
        database=config['mysql_database']
    )
    
    while True:
        try:
            banlist = server.get_ban_list()  # Get the current ban list
            total_rows = db.get_rows()  # Get the total number of rows in the database
            
            for row in range(total_rows):
                data = db.get_data(row)
                
                if data['ID'] not in banlist:  # Check if the player is not already banned
                    server.execute('ban ' + data['ID'])  # Ban the player using their ID
                
            time.sleep(config['check_interval'])
            
        except Exception as e:
            server.logger.error('Error occurred while checking and banning players: {}'.format(str(e)))
            time.sleep(config['check_interval'])

def uban_command(source, args):
    if len(args) < 5:
        return 'Usage: !!uban <playerID> <Reason> <Reason_Text> <isOnline>'
    
    player_id = args[0]
    reason = args[1]
    reason_text = args[2]
    is_online = args[3].lower() == 'true'

	try:
    	player_ip = source.get_player(player_id).player.ping.ip
	except:
		player_ip = "unknown"

    db = MySQLDatabase(
        host=config['mysql_host'],
        user=config['mysql_user'],
        password=config['mysql_password'],
        database=config['mysql_database']
    )
    
    # Add the new row to the database
    db.add_row(player_id, player_ip, reason, reason_text, is_online, source.player)
    
    # Optionally, ban the player immediately
    if is_online:
        source.execute('ban ' + player_id)
    
    return 'Player {} has been banned successfully.'.format(player_id)


def reload_command(source, args):
    # Reload the plugin configuration
    config = server.load_plugin_config()
    if not config:
        config = {
            'mysql_host': 'localhost',
            'mysql_user': 'root',
            'mysql_password': 'password',
            'mysql_database': 'database',
            'check_interval': 3600  # Default check interval is 1 hour
        }
    else:
        pass
    
    return 'Configuration reloaded successfully.'


def on_load(server, old):
    config = server.load_plugin_config()
    if not config:
        config = {
            'mysql_host': 'localhost',
            'mysql_user': 'root',
            'mysql_password': 'password',
            'mysql_database': 'database',
            'check_interval': 3600  # Default check interval is 1 hour
        }
        server.save_plugin_config(config)
    
    server.register_command(
        Literal('uban').then(
            TextArgument('playerID').then(
                TextArgument('Reason', ['hacking', 'stealing', 'destroying', 'other']).then(
                    GreedyTextArgument('Reason_Text').then(
                        BoolArgument('isOnline').runs(uban_command)
                    )
                )
            )
        )
    )
    
    server.register_command(
        Literal('reload').runs(reload_command)
    )
    
    Thread(target=check_and_ban_players, args=(server, config), daemon=True).start()
    server.logger.info('MPWA UnionBan成功启动!')