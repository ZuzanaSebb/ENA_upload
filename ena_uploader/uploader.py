import os
import requests
import sys
import click
from enum import Enum
from xml.etree.ElementTree import Element, SubElement, tostring
from ena_uploader.types._types_and_formats import (
    ENAMetadataSamplesFormat, ENAMetadataSamplesDirFmt,ENAMetadataSamples,
    ENAMetadataStudyFormat, ENAMetadataStudyDirFmt, ENAMetadataStudy,
    ENASubmissionReceiptFormat,ENASubmissionReceiptDirFmt,ENASubmissionReceipt

)

DEV_SERVER_URL =  'https://wwwdev.ebi.ac.uk/ena/submit/drop-box/submit'
PRODUCTION_SERVER_URL = ' https://www.ebi.ac.uk/ena/submit/drop-box/submit'

class ActionType(Enum):
    ADD = "ADD"
    MODIFY = "MODIFY"
    CANCEL = "CANCEL"

def _create_submission_xml(action: ActionType, hold_date: str) -> str:
  
    submission = Element('SUBMISSION')
    actions = SubElement(submission, 'ACTIONS')
    action_element = SubElement(actions, 'ACTION')
    SubElement(action_element, action.value)

    if hold_date:
        hold_action = SubElement(actions, 'ACTION')
        hold = SubElement(hold_action, 'HOLD')
        hold.set('HoldUntilDate', hold_date)

    return tostring(submission, encoding='unicode', method='xml')

def uploadToEna(study: ENAMetadataStudyFormat, 
                samples: ENAMetadataSamplesFormat,
                #username: str = None,
                #password: str = None,
                submission_hold_date: str = '',
                dev: bool = True
                ) -> bytes:
    username = os.getenv('ENA_USERNAME')
    password = os.getenv('ENA_PASSWORD')

    if username is None or password is None:
        raise RuntimeError('Missing username or password, ' +
                           'make sure ENA_USERNAME and ENA_PASSWORD env vars are set')

    print('username = {} password = {}'.format(username, password))

    '''
    Function to sumbmit metedata of the study and samples to ENA.
    Args:
        study : Metadata
                Qiime artifact containing a tsv file with the study atrributes.
        samples : Metadata
                Qiime artifact containing a tsv file with the samples metadata attributes.
        username : Str
                 ENA Webin login username
        password : Str
                 ENA Webin login password
        submission_hold_date: Str
                 The release date of the study, on which it will become public along with all submitted data.
                 By default, this date is set to two months after the date of submission. User can 
                 specify any date within two years of the current date.
        dev : Bool
            True by default. Indicates whether the data submission goes to the development server. If False, the submission 
                goes to the production server. 
    Returns:
        submission_receipt : bytes
                Qiime artifact containing an XML response of  ENA server.
    '''

    url = DEV_SERVER_URL if dev else PRODUCTION_SERVER_URL
    xml_content = _create_submission_xml(action = ActionType.ADD, hold_date = submission_hold_date)

    studyXml = study.toXml()
    samplesXml = samples.toXml();

    with open('study.xml', 'w') as f:
        f.write(str(studyXml))
    with open('samples.xml', 'w') as f:
        f.write(str(samplesXml))

    files = {
    'SUBMISSION': ('submission.xml',  xml_content, 'text/xml'),
    'PROJECT': ('project.xml', studyXml),
    'SAMPLE': ('samples.xml', samplesXml)
       }

    response = requests.post(url, auth=(username, password), files=files)

    with open('response.xml', 'wb') as f:
        f.write(response.content)
    
    return response.content
