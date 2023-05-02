# HVDSA New Members Script

Small flask script for use in Google Cloud Functions that will take two csvs as input
and return a new csv of the rows in the second input csv that weren't in the first. Created for Huron Valley DSA by Elliott K and Sameer P.

These are extremely rough instructions and I can't help if it doesn't work. Ideally this would be set up in a more infra-as-code way so you don't have to
copy/paste into a web editor, but that takes time and energy I don't have :) 

Both CSVs _must_ have a column called `actionkit_id` that can be used to identify the members.

- [Guide on gettings started in Google Cloud Functions](https://cloud.google.com/functions/docs/console-quickstart-1st-gen)

Configuration:
- Create a new Google cloud function, 1st gen
- "Basics"
  - name your function (I just went with 'new-members')
  - Pick a region (I went with us-central1)
- "Trigger"
  - Select 'HTTP' trigger type
  - Select "Allow unauthenticated invocations"
- "Runtime, build, connections and security settings"
  - "Runtime"
    - 256 MB allocated
    - 60 sec timeout
    - Default service account
    - 0 minimum number of instances
    - 10 maximum number of instances
  - Nothing configured from defaults in Build, Connections, or Security and Image repo
- Click Next
- Under "Runtime", select "Python 3.7"
- Use the inline editor to copy the contents `main.py` and `requirements.py` from this repo to `main.py` and `requirements.py` in the cloud function editor
- Remove the noted lines from the start of `main.py` (`app = Flask(__name__)` and `@app.route("/", methods=['POST'])`)
- Set the entry point of the function to `diff_csv`
- Deploy the function
- Done!



Example HTML to call this google cloud function from -- note the `multipart/form-data`:

```html
<form name="FileUpload" method="POST" enctype="multipart/form-data"> 
  <div>
    <label for="file">Select old member csv</label>
    <input type="file" id="file" name="old">
  </div>
  <div>
    <label for="file">Select new member csv</label>
    <input type="file" id="file" name="new">
  </div>
  <div>
    <input type="submit" value="Submit" formaction="https://us-central1-YOUR-PROJECT.cloudfunctions.net/YOUR-FUNCTION-NAME" formmethod="POST"enctype="multipart/form-data" >
  </div>
</form>
```
