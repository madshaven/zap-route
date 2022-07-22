#!/usr/bin/env python3
''' Demonstrating routing StreamLit.
'''

import streamlit as st
from zap_route import ZapRouter


#
#   ROUTES
#

# Initialize the router, set kw to False to disable query url
zr = ZapRouter(query_kw='route')


# Each route should be registered
@zr.register('Index', is_index=True)
def _index():
    st.markdown('# Index page')
    st.info('Welcome to a simple demonstration of routing in StreamLit.')
    st.markdown('''

        Routing between pages can be done with `radio`, `selectbox`, `links`, and/or url `queries`.

        1.  **radio**
            The easiest and most intuitive method is to use radio buttons in the sidebar.
            This is achieved by the method `zr.navigate(position=st.sidebar, method="radio")`.

        2.  **selectbox**
            Alternatively, if there are many pages, use a `selectbox` instead,
            simply by giving the method that as a keyword.
            (And note that the `position` can be anywhere you choose.
            E.g. simply `st` or a given column.)

        3.  **links**
            Any page can be linked, using e.g. `zr.link('Index', position=given_column)`.
            Or all pages can be linked, e.g. at the top of the page:
            `zr.links(positions=given_columns)`.


        4.  **queries**
            The router is initialized to use url queries by e.g. `zr = ZapRouter(query_kw='route')`.
        '''
        )
    st.markdown('Please choose page in the sidebar menu.')


# @zr.register('Information')
# def _information():
#     st.markdown('# Information')
#     st.warning('Please pay close attention!')
#     st.markdown('This is a page where there is not much info. I was lying...')


@zr.register('Queries')
def _queries():
    st.markdown('''
        # Queries

        Here we inspect and modify the url queries.
        Streamlit can change query parameters without rerunning.
        Changing a query from here updates the url, but does not cause a rerun.
        We will need some callbacks here for efficiency.

        Try to perform changes below, or directly in the url!
        But note, the redirect does not take place until a button is pressed.
        '''
        )

    def _del(k):
        params = st.experimental_get_query_params()
        params.pop(k, None)
        st.experimental_set_query_params(**params)

    def _set(k, v):
        params = st.experimental_get_query_params()
        params[k] = v
        st.experimental_set_query_params(**params)

    # Modify existing content
    st.write('')
    for k, v in st.experimental_get_query_params().items():
        c1, c2 = st.columns([10,3])
        key = f'inp_{k}'
        label = f'Content of "{k}"'
        n = c1.text_input(label=label, value=v[0], key=key)
        _set(k, n)

        c2.markdown('#')
        c2.button(f'Delete "{k}"', on_click=_del, args=(k,))

    # Write new content
    c1, c2, c3 = st.columns([3, 7, 3])
    k = c1.text_input(label='key', value='new_query')
    v = c2.text_input(label='value')
    c3.markdown('#')
    c3.button(f'Add "{k}"', on_click=_set, args=(k, v))

    st.markdown('')
    st.button('Re-run!')


# Routes do not have to be registered by decoration...
def _links():

    # Add header, if needed
    # The links here are just to show flexibility, they are not so pretty
    cols = st.columns([len(r)+6 for r in zr.routes.keys()])
    zr.links(positions=cols)
    st.markdown('---')


    st.markdown('''
        # Links

        This page demonstrates links to all pages in the header.
        These can alternatively be placed in the sidebar, or at any other positions.

        We also demonstrate how to make links to given pages.
        '''
        )

    # positions for links
    c1, c2, c3, _ = st.columns((4, 6, 10, 15))

    # Built in
    zr.link('Index', position=c1)
    # Manual
    c2.button('Goto Index', on_click=zr.set_route, args=('Index',))
    # Manual
    c3.button('Self referential...', on_click=zr.set_route, args=('Links',))


# ... you can also add the routes explicitly
zr.routes['Links'] = _links

# ... and/or set the index explicitly
# zr.index = 'Links'


#
#   BUILD PAGE
#

# Display top of sidebar
st.sidebar.markdown('''
    # Router demonstration

    by [Inge Madshaven](https://github.com/madshaven)
    ''')

# Navigation in sidebar
st.sidebar.markdown('')
# st.sidebar.markdown('''
#     The radio buttons is generally preferable method for navigation.
#     The combination of a selectbox and links is a nice way of navigation.
#     ''')
zr.navigate(position=st.sidebar, method='selectbox', label='Navigate by selectbox')
zr.navigate(position=st.sidebar, method='radio', label='Navigate by radio buttons')
st.sidebar.markdown('''<sub>Explicit link</sub>''', unsafe_allow_html=True)
st.sidebar.button('Index', on_click=zr.set_route, args=('Index',))

# Add header, if needed
# st.markdown('Header')
# st.markdown('---')

# Render the actual page
zr()

# Display sidebar footer
# st.sidebar.markdown('Footer')
# st.sidebar.button('Re-run!')

# Add main footer, if needed


#
