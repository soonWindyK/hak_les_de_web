from databaseModules.classUsersDB import UsersDB_module
from flask import render_template, redirect, session
from databaseModules.classCityRegionDB import CityRegionDB_module
from databaseModules.classSmallFuncsDB import SmallFuncsDB_module
from databaseModules.classNkoDB import NkoDB_module


def nko_add(request):
    cities_list = CityRegionDB_module().get_cities_list_with_region()
    cats_list = SmallFuncsDB_module().select_all_categories()

    if request.method == 'POST':
        action = request.form.get('action', None)
        if action == 'btn-create-nko':
            request = request.form
            form_data = {
                    'name': request['name'],
                    'category': request['category'],
                    'description': request.get('description', ''),
                    'about': request.get('about', ''),
                    'volunteer_activities': request.get('volunteer_activities', ''),
                    'address': request.get('address', ''),
                    'email': request['email'],
                    'phone': request.get('phone', ''),
                    'social_media': request.get('social_media', ''),
                    'website': request.get('website', ''),
                    'city': request['city'],
                }

            form_data['category'] = form_data['category'].split("_")[-1]
            form_data['city'] = form_data['city'].split("_")[-1]
            print(form_data.values())
            result = NkoDB_module().create_nko(data=tuple(form_data.values()))
            print(result)
            if result:
                result = str(result)
                if '`FK_citi_code_nko`' in result:
                    return render_template('nko-add.html',
                                           cats_list=cats_list, cities_list=cities_list, form_data=form_data,
                                           error_msg='Выберите город!'
                                           )

                if 'FK_category_id`' in result:
                    return render_template('nko-add.html',
                                           cats_list=cats_list, cities_list=cities_list, form_data=form_data,
                                           error_msg='Выберите категорию!'
                                           )


            #     print(result.replace('', 'error'))
            #
            #
            # print(request)
            return render_template('nko-add.html', cats_list=cats_list,
                                   cities_list=cities_list, form_data=form_data)

    return render_template('nko-add.html', cats_list=cats_list, cities_list=cities_list)