from typing import List, Dict, Tuple


def id_and_visit_from_filename(filename: str) -> Tuple[int, int]:
    """ Extract the SOF ID and the visit from a given DICOM filename
    :param filename: filenamne of a .dcm file
    :return: (id: int, visit: int) SOF id and visit as encoded in the filename
    """
    import re
    pattern = "SF([0-9]+)V([0-9]+)H.dcm"
    match = re.match(pattern, filename)
    return int(match.groups()[0]), int(match.groups()[1])


def read_label_file(filename: str) -> List[Dict]:
    """ Reads proximal femur detection labels from a label-studio json file and returns
        it's content in a cleaned up way.
    :param filename: Path to a label-studio json file
    :return: List of dictionary containing the information:
        (id: str, flipped: int, left_incomplete: int, left_incomplete_shaft:int, left_implant,
         right_incomplete: int, right_incomplete_shaft:int, right_implant,
         left_bbox_x: float, left_bbox_y: float, left_bbox_w: float, left_bbox_h: float,
         right_bbox_x: float, right_bbox_y: float, right_bbox_w: float, right_bbox_h: float) where the id
         is stored in the format <SOF_ID>V<Visit> and all int values are either 0 (false/absent) or 1 (true/present).
         The bbox coordinates are given in absolute pixel coordinates.
    """
    import json
    import re

    labels = []
    with open(filename, 'r')as fh:
        for item in json.load(fh):
            image_id = re.match('.*/[a-zA-Z0-9]+-([0-9]+V[0-9])\.png', item['data']['image']).groups()[0]
            entry = {
                'id': image_id,
                'flipped': 0,
                'left_incomplete': 0,
                'left_incomplete_shaft': 0,
                'left_implant': 0,
                'right_incomplete': 0,
                'right_incomplete_shaft': 0,
                'right_implant': 0
            }
            rects = []
            for field in item['completions'][0]['result']:
                if field['from_name'] == 'orientation':
                    entry['flipped'] = 0 if field['value']['choices'][0] == 'default' else 1
                elif field['from_name'] == 'salience_left':
                    entry['left_incomplete'] = 1 if 'Incomplete' in field['value']['choices'] else 0
                    entry['left_incomplete_shaft'] = 1 if 'Shaft Incomplete' in field['value']['choices'] else 0
                    entry['left_implant'] = 1 if 'Implant' in field['value']['choices'] else 0
                elif field['from_name'] == 'salience_right':
                    entry['right_incomplete'] = 1 if 'Incomplete' in field['value']['choices'] else 0
                    entry['right_incomplete_shaft'] = 1 if 'Shaft Incomplete' in field['value']['choices'] else 0
                    entry['right_implant'] = 1 if 'Implant' in field['value']['choices'] else 0
                elif field['from_name'] == 'prox_femur':
                    rects.append((field['value']['x'], field['value']['y'],
                                  field['value']['width'], field['value']['height']))

            rects = rects if rects[0][0] < rects[1][0] else [rects[1], rects[0]]
            entry['left_bbox_x'] = rects[0][0]
            entry['left_bbox_y'] = rects[0][1]
            entry['left_bbox_w'] = rects[0][2]
            entry['left_bbox_h'] = rects[0][3]
            entry['right_bbox_x'] = rects[1][0]
            entry['right_bbox_y'] = rects[1][1]
            entry['right_bbox_w'] = rects[1][2]
            entry['right_bbox_h'] = rects[1][3]

            labels.append(entry)

    return labels
