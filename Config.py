
import ConfigParser
import os

g_currentDir = os.path.dirname(os.path.abspath(__file__))
print(g_currentDir)

g_config = ConfigParser.ConfigParser()
g_config.read(g_currentDir + "/app.properties")
