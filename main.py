import pandas as pd
from datetime import datetime
from flask import Response, Flask, request
import re
import io

# For use in GCF, remove this line
app = Flask(__name__)
# And remove this line (GCF already has flask initialized / routed)
@app.route("/", methods=['POST'])
def diff_csv():
  if 'old' not in request.files:
      return "No old member file uploaded", 400

  if 'new' not in request.files:
      return "No new member file uploaded", 400

  old_file = request.files["old"]
  new_file = request.files["new"]

  if old_file.filename == '':
      return "No file found", 400
    
  if new_file.filename == '':
      return "No file found", 400

  key = "AK_ID"

  old_df = pd.read_csv(old_file, index_col=key).reset_index().set_index(key)
  new_df = pd.read_csv(new_file, index_col=key).reset_index().set_index(key)

  diff_file  = pd.merge(new_df, old_df, left_on=key, how="outer", right_index=True, indicator=True, suffixes=[None, "_y"])
  diff_file = diff_file[diff_file['_merge'] == 'left_only']

  diff_file = diff_file.drop(['_merge'], axis=1)
  diff_file = diff_file.filter(regex=".*(?<!_y)$", axis=1)

  diff_file = diff_file.reset_index()
  diff_file = diff_file.drop(['index'], axis=1, errors='ignore')

  # Name the file with a timestamp.
  now = datetime.now()
  filename = "hvdsa_new_members_%s.csv" %(now.strftime("%Y%m%d%H%M%S"))
  
  #dump the dataframe to the output string buffer
  output = io.StringIO()
  diff_file.to_csv(path_or_buf=output,sep=',',float_format='%.2f',index=False,decimal=",")

  #return the output string buffer as a csv
  response = Response(output.getvalue(), mimetype="text/csv", content_type='csv')
  response.headers['Content-Disposition'] = 'attachment; filename=%s' %(filename)
  return response