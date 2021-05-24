#@auto-fold regex /./
import sys,pandas as pd, requests as re
import env
## NOTE: APi documentation https://monday.com/developers/v2#introduction-section
wb = env.open_wb('')
sh = wb.worksheet('')

def request(query):
	"""Create a request to Monday.com API"""
	headers = {"Authorization" : env.m_key} # set headers
	URL = "https://api.monday.com/v2"
	data = {"query" : query}
	r = re.get(url=URL, json=data, headers=headers) # make request
	if r.status_code == 401:
		print('Status: ', r.status_code)
		raise PermissionError("Check your API key!")
	if r.status_code != 200:
		print('Status:', r.status_code)
		raise ValueError("Check your query contents!")
	if ("error" in r.json().keys()):
		print(r.json())
		raise SyntaxError("Check your query syntax!")
	else:
		results = r.json()
		return results

def queryboard(board, page=1):
	"""Query board and return the fields below"""
	query = """
            query {
                boards (ids: %s limit: 20, page: 1) {
    id
    name
    columns
    {
        title
        id
    }
    items (limit: 1000, page: %s)
    {name
        column_values
        {
            # id
            title
            # value
            text
        }
    group{title}
    }
	}}""" % (board,page)
	return  request(query)

def board_to_df(board):
	"""Send the response data into a DataFrame"""
	df =  pd.DataFrame()
	for i in range(1,8): #pagination
		try:
			results = queryboard(board, i)
			for item in results['data']['boards']: #update the dict with new keys and values
				item['columns'].insert(0,{'title': 'Group', 'id': 'Group'})
				item['columns'].insert(0,{'title': 'Load Date', 'id': 'Load Date'})
			for item in  results['data']['boards'][0]['items']:
				item['column_values'].insert(0,{'title': 'Name', 'text': item['name']})
				item['column_values'].insert(0,{'title': 'Group', 'text': item['group']['title']})
				item['column_values'].insert(0,{'title': 'Load Date', 'text': env.now(1)})
				results['data']['boards'][0]['items'][0]
			#append & transpose data into new DataFrame
			for items in results['data']['boards'][0]['items']:
				df = df.append(pd.DataFrame(items['column_values']).T[1:])
		except:
			continue
	df.columns = pd.DataFrame(results['data']['boards'][0]['columns']).T.iloc[0]
	df =df.reset_index(drop=True)
	return df

def send_to_sheets():
	"""Send DataFrame to google sheets"""
	for boards in sh.get_all_values()[1:]:
		try:
			print('working on {}'.format(boards[1]))
			df = board_to_df(boards[0])
			env.rep_data_sh(df,wb.id,boards[1],df.shape[1])
		except:
			print('Error on {}'.format(boards[1]))
			continue
	return ['Monday board exporter job completed successfully']

results = send_to_sheets()
