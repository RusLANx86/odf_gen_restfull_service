from odf.opendocument import load, OpenDocument
from odf_gen.return_odf_element import update_odf_element


def fill_template(template_file_path:str, json_data:dict) -> OpenDocument:
    file = load(template_file_path)
    text = file.text

    def update_user_fields(odf_element):
        for odf_elem in odf_element.childNodes:
            try:
                user_field_name = odf_elem.getAttribute("name")
                data = json_data.get(user_field_name)
                if data != None:
                    res = update_odf_element(element=odf_elem, data=data)
                    try:
                        styles = res["styles"]
                        for style in styles:
                            file.automaticstyles.addElement(style)
                    except:
                        pass
            except:
                update_user_fields(odf_elem)

        return odf_element

    update_user_fields(odf_element=text)

    return file
