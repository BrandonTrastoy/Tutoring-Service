import pandas as pd
from pandas import DataFrame
from datetime import date

def readExel():
	df = pd.read_excel('test.xlsx')
	df = pd.DataFrame(df)
	return df

def addStudentBackend(givenArray):
	df = readExel()
	a = givenArray
	#print(a)
	name = a[0]
	session = a[1]
	date = a[2]
	amount = a[3]
	payment_status = a[4]

	data = [{'Date':date,'Name':name, 'Session Length':session,'Amount':amount,'Payment Status': payment_status}]
	df = df.append(data,ignore_index=True,sort=False)
	df.to_excel('test.xlsx', index = False)
	return df

def studentList():
	df = readExel()
	listStudent = df["Name"].unique()
	listStudent = list(listStudent)
	return listStudent

def filterStudentInfo(name, status):
	df = readExel()

	if name == "All":
		filteredInfo = df.loc[(df['Payment Status'] == status)]
	else:
		filteredInfo = df.loc[(df['Name'] == name) & (df['Payment Status'] == status)]

	temp = str(filteredInfo)

	if "Empty DataFrame" in temp:
		return "No Data Found\n"
	else:
		return temp

def allStudentInfoList():
	
	studentInfoList = []

	listOfIds = idList()
	
	for singleId in listOfIds:
		studentInfoList.append(singleStudentWithId(singleId))
	
	return studentInfoList

def singleStudentWithId(id):
	df = readExel()

	name = df['Name'][id]
	session = df['Session Length'][id]
	date = str(df['Date'][id])
	amount = df['Amount'][id]
	status = df['Payment Status'][id]

	singleStudent = [id, name, session, date, amount, status]
	
	return  singleStudent

def idList():
	df = readExel()
	idList = list(df.index)
	return idList

def singleStudent(id):
	df = readExel()
	
	name = df['Name'][id]
	session = df['Session Length'][id]
	date = str(df['Date'][id])
	amount = df['Amount'][id]
	status = df['Payment Status'][id]

	singleStudent = [name, session, date, amount, status]
	
	return  singleStudent

def updateStudent(studentID, fieldArray):
	df = readExel()
	name = fieldArray[0]
	session = fieldArray[1]
	date = fieldArray[2]
	amount = fieldArray[3]
	payment_status = fieldArray[4]
	df.loc[studentID, 'Name'] = name
	df.loc[studentID, 'Session Length'] = session
	df.loc[studentID, 'Date'] = date
	df.loc[studentID, 'Amount'] = amount
	df.loc[studentID, 'Payment Status'] = payment_status

	df.to_excel('test.xlsx', index = False)