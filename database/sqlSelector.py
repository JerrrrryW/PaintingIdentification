import mysql.connector
import cv2
from PyQt5.QtWidgets import QApplication

from echarts.relativeGraphTest import initPyQtGraph

# create a connection to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="MYSQL1220",
    database="capat"
)

# create a cursor to execute SQL queries
mycursor = mydb.cursor()

def findPidBySid(sid: str):
    mycursor.execute("SELECT P_S.pid, name FROM P_S, paintings WHERE P_S.sid = %s and P_S.pid = paintings.pid;", (sid,))
    result = mycursor.fetchall()
    return result

def findRelativeEntities(queryid: str):
    result = []
    if queryid.startswith('p') or queryid.startswith('P'):
        mycursor.execute("SELECT name FROM paintings WHERE pid = %s;", (queryid,))
        pResult = mycursor.fetchall()
        result.append({'id': queryid, 'content': pResult[0][0], 'type': '绘画', 'link': 0})

        mycursor.execute("SELECT iid, content FROM Inscriptions WHERE Inscriptions.pid = %s;", (queryid,))
        iResult = mycursor.fetchall()
        for iid in iResult:
            result.append({'id': iid[0], 'content': iid[1], 'type': '题款', 'link': queryid})

        mycursor.execute("SELECT P_S.sid, name FROM P_S, seals WHERE P_S.pid = %s and p_s.sid = seals.sid;", (queryid,))
        sResult = mycursor.fetchall()
        for sid in sResult:
            result.append({'id': sid[0], 'content': sid[1], 'type': '印鉴', 'link': queryid})
            sub_result = findPidBySid(sid[0])
            for pid in sub_result:
                if pid[0].lower() != queryid.lower():
                    result.append({'id': pid[0], 'content': pid[1], 'type': '绘画', 'link': sid[0]})

    elif queryid.startswith('y') or queryid.startswith('Y'):
        mycursor.execute("SELECT name FROM seals WHERE sid = %s;", (queryid,))
        sResult = mycursor.fetchall()
        result.append({'id': queryid, 'content': sResult[0][0], 'type': '印鉴', 'link': 0})

        pResult = findPidBySid(queryid)
        for pid in pResult:
            result.append({'id': pid[0], 'content': pid[1], 'type': '绘画', 'link': queryid})
            result.extend(findRelativeEntities(pid[0]))

    elif queryid.startswith('t') or queryid.startswith('T'):
        mycursor.execute("SELECT content FROM inscriptions WHERE iid = %s;", (queryid,))
        iResult = mycursor.fetchall()
        result.append({'id': queryid, 'content': iResult[0][0], 'type': '题款', 'link': 0})

        mycursor.execute("SELECT Paintings.pid, name FROM Inscriptions, paintings WHERE Inscriptions.iid = %s and paintings.pid = Inscriptions.pid;", (queryid,))
        pResult = mycursor.fetchall()
        for pid in pResult:
            result.append({'id': pid[0], 'content': pid[1], 'type': '绘画', 'link': queryid})
            result.extend(findRelativeEntities(pid[0]))

    return result


def truncate_string(s, n):  # Truncates string s to n characters with an ellipsis if needed.
    if len(s) > n:
        return s[:n] + '...'
    else:
        return s

def convert_to_nodes_and_links(data):
    nodes = []
    links = []
    node_names = set()
    for item in data:
        node_id = item["id"]
        node_type = item["type"]
        node_link = item["link"]
        node_content = item["content"]
        # Add node to nodes list
        if node_id not in node_names:
            nodes.append({"name": node_id, "symbolSize": 20, "value": truncate_string(node_content, 12), "category": node_type})
            node_names.add(node_id)
        else:
            for node in nodes:
                if node["name"] == node_id:
                    node["symbolSize"] += 5
                    break
        # Add link to links list
        if node_link != 0:
            links.append({"source": node_id, "target": node_link})
    return nodes, links


if __name__ == "__main__":
    result = findRelativeEntities('y12')
    print(result)
    nodes, links = convert_to_nodes_and_links(result)
    print('nodes:', nodes)
    print('links:', links)
    app = QApplication([])
    view = initPyQtGraph(nodes, links, [{"name": "绘画"}, {"name": "题款"}, {"name": "印鉴"}])
    view.show()
    app.exec_()

