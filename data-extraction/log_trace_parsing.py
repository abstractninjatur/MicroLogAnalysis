import base64

from elasticsearch import Elasticsearch
from schema import Tracing_pb2
import pandas as pd

ELASTIC_SEARCH_HOST = Elasticsearch('http://3.94.54.180:30092')


def convert_protobuf_to_dict(pb_obj):
    result = {}
    for field in pb_obj.DESCRIPTOR.fields:
        value = getattr(pb_obj, field.name)
        if field.type == field.TYPE_MESSAGE:  # Nested protobuf
            if field.label == field.LABEL_REPEATED:
                result[field.name] = [convert_protobuf_to_dict(item) for item in value]
            else:
                result[field.name] = convert_protobuf_to_dict(value)
        elif field.type == field.TYPE_ENUM:
            result[field.name] = field.enum_type.values_by_number.get(value).name
        else:
            result[field.name] = value
    return result


def parse_binary_data(binary_data):
    trace_segment_object = Tracing_pb2.SegmentObject()
    try:
        trace_segment_object.ParseFromString(binary_data)
        return trace_segment_object
    except Exception as e:
        print("Error parsing binary data:", e)
        return None


def parse_trace_data_to_csv_row(document):
    binary_data = base64.b64decode(document['_source']['data_binary'])
    parsed_data = parse_binary_data(binary_data)
    parsed_data = convert_protobuf_to_dict(parsed_data)

    lst = []
    for span in parsed_data['spans']:
        lst.append({
            'traceId': parsed_data['traceId'],
            'traceSegmentId': parsed_data['traceSegmentId'],
            'startTime': span['startTime'],
            'parentSpanId': span['parentSpanId'],
            'spanId': span['spanId'],
            'endTime': span['endTime'],
            'operationName': span['operationName'],
            'peer': span['peer'],
            'spanType': span['spanType'],
            'spanLayer': span['spanLayer'],
            'componentId': span['componentId'],
            'isError': span['isError'],
            'service': parsed_data['service']
        })

    return lst


###
# This method contains logic to fetch the documents from es
# This method get the documents ingested in last 1m and scrolls
# till all the documents fetched beyond the fault size 10000
##
def get_data_from_index(index_name, query=None, size=10000, scroll_time='1m'):
    if query is None:
        query = {"query": {"match_all": {}}}

    # Initialize the scroll
    page = ELASTIC_SEARCH_HOST.search(index=index_name, body=query, scroll=scroll_time, size=size)
    scroll_id = page['_scroll_id']
    hits = page['hits']['hits']

    # Start scrolling
    while len(page['hits']['hits']):
        page = ELASTIC_SEARCH_HOST.scroll(scroll_id=scroll_id, scroll=scroll_time)
        scroll_id = page['_scroll_id']
        hits.extend(page['hits']['hits'])

    # Clear the scroll when done
    ELASTIC_SEARCH_HOST.clear_scroll(scroll_id=scroll_id)

    return hits


###
# This method aggregate each line of the log data recived from es
#
##
def save_log_data_in_file(data,folder_name):
    log_rows = []
    for doc in data:
        if doc:
            log_rows.append(doc['_source']['content'])

    with open(f"{folder_name}/log-data.log", 'w', encoding='utf-8') as file:
        for entry in log_rows:
            file.write(entry)


###
# This method aggregate  each line of the trace data recived from es
#
##
def save_trace_data_in_file(data,folder_name):
    csv_rows = []
    for doc in data:
        row = parse_trace_data_to_csv_row(doc)
        if row:
            csv_rows.extend(row)

    df = pd.DataFrame(csv_rows)
    df.to_csv(f'{folder_name}/trace-data.csv', index=False)


###
#  This method has the name of the log and
#  trace index to get and call the parsing method
#
###

def dump_trace_log_data():
    save_trace_data_in_file(get_data_from_index("sw_segment-20231215"),"20231215")
    save_log_data_in_file(get_data_from_index("sw_log-20231215"),"20231215")


if __name__ == "__main__":
    dump_trace_log_data()
