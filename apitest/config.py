DB_USER = 'postgres'
DB_PW = 'urmilaa'
DB_NAME = 'redcarpetup'
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=DB_USER, pw=DB_PW, url='localhost', db=DB_NAME)
