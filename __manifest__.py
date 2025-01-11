# -*- coding: utf-8 -*-
{
    'name': "Basic Powered Scaffold",
    'summary': """ Short (1 phrase/line) """,
    'description': """ Long description """,
    'author': "Basic-Powered",
    'website': "https://site.basic-powered.com",
    'category': 'Uncategorized',
    'version': '0.0',
    'depends': ['base'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],

    'license': 'Other proprietary',

}

# Please specify the licence type of this module before you upload it.
# for the license field above set it as: 
#     - "Other OSI approved licence" if for MIT and Apache license.
#     - "GPL-3 or any later version" for GPL license.
#     - "Other proprietary" for private licance.

# - if the module is private then just open the licence file at the root of the module directory
#     and change the project name of the private licence then delete this string and upload the module. 

# - if the module is public then delete the licance file and add one of the licenses specified below
#     from github GUI after uploading the module and delete this string.

#     - MIT : It's a Do whatever you want with my stuff, just don't sue me type of license.
#             Choose it if you're afraid of nobody using your software.

#     - Apache : Same as MIT but with more words. Great for lawyers.
#                 Choose it over the MIT if you're afraid of Patent Trolling.

#     - GPL : Choose this if you're afraid of people using your work in an unfair way (e.g. make money on your back bothers you). 
#             If they use your software, they will have to use the same license as you (i.e. probably open-source it).

# to add a license form Github GUI:
#     - after uploading the module click "Add file" and then click "Create new file".
#     - name the new file LICENSE.md, a new option should appear with the name "Choose a license template".
#     - click "Choose a license template" and then choose one of the licenses from the left of the screen (first three).
#     - if you chose the MIT license then use the year 2021.
#     - click on "Review and submit" and then commit the changes on the license file.