import mysql.connector
import cv2

# create a connection to the MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="MYSQL1220",
  database="capat"
)

# create a cursor to execute SQL queries
mycursor = mydb.cursor()

# find the pid of the painting containing the given Iid
iid = "I123"
mycursor.execute("SELECT pid FROM Inscriptions WHERE Iid = %s", (iid,))
result = mycursor.fetchone()
if result:
  pid = result[0]
  print("The pid of the painting containing the inscription with Iid", iid, "is", pid)
else:
  print("No painting found containing the inscription with Iid", iid)

# find the pid of all paintings containing the given Sid
sid = "S456"
mycursor.execute("SELECT pid FROM P_Y WHERE yid = %s", (sid,))
results = mycursor.fetchall()
if results:
  pids = [result[0] for result in results]
  print("The following pids are associated with the seal with yid", sid, ":", pids)
else:
  print("No paintings found containing the seal with yid", sid)

# display all found painting image(s)
if pid:
  img = cv2.imread(pid + ".jpg")
  cv2.imshow("Painting Image", img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

if pids:
  for pid in pids:
    img = cv2.imread(pid + ".jpg")
    cv2.imshow("Painting Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
