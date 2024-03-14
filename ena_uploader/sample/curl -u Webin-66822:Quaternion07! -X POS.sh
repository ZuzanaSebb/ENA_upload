curl -u Webin-66822:Quaternion07! -X POST 'https://wwwdev.ebi.ac.uk/ena/dev/submit/webin-v2/submit/' \
-H 'Accept: application/xml' \
-H 'Content-Type: application/xml' \
-T 'test2.xml'


curl -u Webin-66822:Quaternion07! -X POST ''https://wwwdev.ebi.ac.uk/ena/dev/submit/webin-v2/submit/queue' \
-H 'Accept: application/xml' \
-H 'Content-Type: application/xml' \
-T 'test2.xml'

curl -uWebin-66822:Quaternion07! "https://www.ebi.ac.uk/ena/submit/webin-v2/submit/poll/ERA16500666" \
-H 'Accept: application/xml'


curl -u Webin-66822:Quaternion07! -X POST 'https://wwwdev.ebi.ac.uk/ena/dev/submit/webin-v2/submit/queue' \
-H 'Accept: application/xml' \
-H 'Content-Type: application/xml' \
-T 'test2.xml'
