from flask import Flask,redirect,request,render_template
import requests
import json

app=Flask(__name__)
config = app.config

@app.route('/')
def home():
    #select all user's item.
    return redirect('https://id.twitch.tv/oauth2/authorize?client_id=45c2yhxzp8cr8m3p9g9eiuqvqf0ukf&force_verify=false&redirect_uri=http://localhost:5000/game&response_type=code&&scope=user:read:email+user:read:follows+chat:read+chat:edit+channel:moderate+channel:read:subscriptions+channel:manage:redemptions+channel:read:redemptions+moderation:read+bits:read+moderator:manage:banned_users+user:read:blocked_users+user:manage:blocked_users+channel:manage:moderators+moderator:manage:announcements+moderator:manage:shoutouts+moderator:read:followers+moderator:manage:chat_messages+channel:manage:broadcast+channel:manage:raids', code=302)

@app.route('/game',methods=['GET'])
def game():
    #use twitch api by flask.
    if request.method == 'GET':
        errorReason = request.args.get('error')
        code = request.args.get('code')
        scope = request.args.get('scope')
        state = request.args.get('state')
        if errorReason is not None:
            return errorReason
        elif code is not None:
            oauth2Url = 'https://id.twitch.tv/oauth2/token'
            oauth2Obj = {
                'client_id':'45c2yhxzp8cr8m3p9g9eiuqvqf0ukf',
                'client_secret':'ztg5d71akqjrgrqazgl74rrmrsdz7r',
                'code':code,
                'grant_type':'authorization_code',
                'redirect_uri':'http://localhost:5000/result'
            }
            print('='*20)
            print(code)
            oauth2Data = requests.post(oauth2Url, data = oauth2Obj)
            oauth2Json = oauth2Data.json()
            access_token = oauth2Json['access_token']
            # print(oauth2Json)
<<<<<<< HEAD
            # userData = requests.get('https://api.twitch.tv/helix/users', headers = {'Authorization': f'Bearer {access_token}','Client-ID':f'{oauth2Obj["client_id"]}'})
            # userDataJson = userData.json()['data'][0]
            # print(userDataJson)
            # return render_template('test.html',data=userDataJson)
=======
            userData = requests.get('https://api.twitch.tv/helix/users', headers = {'Authorization': f'Bearer {access_token}','Client-ID':f'{oauth2Obj["client_id"]}'})
            userDataJson = userData.json()['data'][0]
            # print(userDataJson)
            return render_template('test.html',data=userDataJson, access_token=access_token)
>>>>>>> 4df75e67c6e0664e443e1a9578d0e5529d753f1b
    return 'ERROR'

@app.route('/result')
def result():
    oauth2Url = 'https://id.twitch.tv/oauth2/token'
    oauth2Obj = {
        'client_id':'45c2yhxzp8cr8m3p9g9eiuqvqf0ukf',
        'client_secret':'ztg5d71akqjrgrqazgl74rrmrsdz7r',
        'grant_type':'client_credentials',
    }

    oauth2Data = requests.post(oauth2Url, data = oauth2Obj)
    oauth2Json = oauth2Data.json()
    access_token = oauth2Json['access_token']
    print(oauth2Json)
    userData = requests.get('https://api.twitch.tv/helix/users', headers = {'Authorization': f'Bearer {access_token}','Client-ID':f'{oauth2Obj["client_id"]}'})
    userDataJson = userData.json()
    print(userDataJson)
    return render_template('test.html',data=userDataJson,access_token=access_token)


if __name__ == '__main__':
    app.run(debug=True)