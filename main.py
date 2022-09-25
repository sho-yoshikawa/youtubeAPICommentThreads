import requests
import json


URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
VIDEO_ID = "4Ei2ycRd6fE"

path = "./my_api.txt"
f = open(path)
API_KEY = f.read()
f.close()


def printJsonData(res):
	res = json.dumps(res, indent=4)
	print(res)


def printTopComments(topComments, n):
	cnt = 0
	for topComment in topComments:
		if 10 < cnt:
			break
		print("==============================")
		print(topComment[1])
		print("高評価数： ", topComment[0])
		print("==============================")
		cnt += 1


def getResponse(next_page_token=None):
	params = {
		'key': API_KEY,
		'part': 'snippet',
		'videoId': VIDEO_ID,
		'order': 'relevance',
		'textFormat': 'plaintext',
		'maxResults': 1000,
		'pageToken': next_page_token
	}
	res = requests.get(URL, params=params)
	data = res.json()
	return data

def extractComments(res, comments):
	comments_info = res["items"]
	for comment_info in comments_info:
		comment = comment_info['snippet']['topLevelComment']['snippet']['textDisplay']
		like = comment_info['snippet']['topLevelComment']['snippet']['likeCount']
		comments.append([like, comment])
	return comments
	


def getAllComments(res):
	comments = []
	comments = extractComments(res, comments)
	next_page_token = res["nextPageToken"]
	# デカすぎを防ぐために数字で調整
	for _ in range(10):
		res = getResponse(next_page_token=next_page_token)
		comments = extractComments(res, comments)
		try:
			next_page_token = res["nextPageToken"]
		except:
			pass
		if next_page_token is None:
			break
	return comments


def sortCommentsByLikes(comments):
	topComments = sorted(comments, reverse=True)
	return topComments


def main():
	res = getResponse()
	comments = getAllComments(res)
	print(len(comments))
	topComments = sortCommentsByLikes(comments)
	printTopComments(topComments, 10)


if __name__ == "__main__":
	main()
