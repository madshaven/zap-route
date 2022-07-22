#!/usr/bin/env python3
''' Tools for managing pages.
'''

import streamlit as st
from urllib.parse import unquote


#
#   ROUTER
#


class ZapRouter:

    def __init__(s, query_kw=False, index=None):

        # store pages in a dict(key: render_function)
        s.routes = {}

        # index page
        # defaults to first registred page
        # is the default redirect if a page is not found
        s.index = index

        # keyword used in query url
        # set to false to disable query url
        s.query_kw = 'route' if query_kw is True else query_kw

    def __call__(s, key=None):
        # render a page, defaults to the current route
        # idea: default to index or
        if key is None:
            key = s.get_route()
        if key in s.routes:
            s.routes[key]()
        else:
            s.fourohfour(key)

    def fourohfour(s, route):
        st.warning(f'404 page not found')
        s.link(route=s.index, label='Take me to the index!')

    def __len__(s):
        return len(s.routes)

    def register(s, key, is_index=False):
        # return decorator to register route

        # set index page
        # defaults to fist registred page, if not set
        if (s.index is None) or is_index:
            s.index = key

        # decorator to return
        def _w(f):
            s.routes[key] = f   # register the route
            return f            # return function untouched
        return _w

    def get_query_route(s):
        # return the route set by query url

        # do not look if no kw is set
        if s.query_kw:
            # get route from query url
            params = st.experimental_get_query_params()
            route = params.get(s.query_kw, None)
            route = route[0] if (type(route) == list) else route
            route = unquote(route) if (route is not None) else route
        else:
            # None should give the index
            route = None

        return route

        # No
        # # Check if valid, or redirect to index
        # if (route is None) or (route in s.routes):
        #     return route
        # else:
        #     # Warn, since this means query was wrong
        #     st.warning(f'Not possible to go to: {route}')
        #     st.info(f'Redirecting to index.')
        #     return None

    def set_query_route(s, route):
        # set the query route (or remove it, if needed)
        params = st.experimental_get_query_params()
        if s.query_kw:
            params[s.query_kw] = route
        else:
            params.pop(s.query_kw, None)
        st.experimental_set_query_params(**params)

    def get_zap_route(s):
        # get the internal route

        # ensure/initialize session state
        if 'zap_route' not in st.session_state:
            st.session_state.zap_route = None

        # default to index, if needed
        if st.session_state.zap_route is None:
            st.session_state.zap_route = s.index

        # redirect to index, if needed
        if st.session_state.zap_route not in s.routes:
            st.info(f'Redirecting to index.')
            st.session_state.zap_route = s.index
        return st.session_state.zap_route

    def set_zap_route(s, route):
        # set the session state route
        st.session_state.zap_route = route

    def get_route(s):
        # get the route, check query url then internal state
        route = s.get_query_route()
        if route is None:
            route = s.get_zap_route()

        # update the route, can be needed for query
        s.set_route(route)
        return route

    def set_route(s, route):
        # set the internal and query url route
        # this decides the route on next reload
        # use e.g. as callback
        if route in s.routes:
            s.set_zap_route(route)
            s.set_query_route(route)
        else:
            pass
            # st.warning(f'Unable to set route: {route}')

    def route(s, route):
        # use as callback for link/route to new page
        return s.set_route(route)

    def link(s, route, position=st, label=None, key=None):
        # create a button linking to a page
        label = route if (label is None) else label
        key = f'link2{route}' if (key is None) else key
        position.button(
            label=label,
            key=key,
            on_click=s.set_route,
            kwargs={'route': route},
            )

    def links(s, routes=None, positions=None, labels=None, keys=None):
        # create buttons linking to all pages
        if routes is None:      routes = s.routes.keys()
        if labels is None:      labels = routes
        if positions is None:   positions = st
        if type(positions) is not list:   positions = [positions] * len(routes)
        if keys is None:        keys = [f'links2{r}{p}' for r, p in zip(routes, positions)]
        for r, p, l, k in zip(routes, positions, labels, keys):
            s.link(r, p, l, k)

    def navigate(s, method='radio', position=st.sidebar, label='Navigate routes'):
        # create a widget for navigation

        # initialize the widget state to current route
        route = s.get_route()
        key = f'router_choose_{method}_{label}'

        # fixme: should be handled better?
        if route in s.routes.keys():
            st.session_state[key] = route

        # widget callback to change route
        def cb():
            s.set_route(st.session_state[key])

        # widget kwargs
        kwargs = dict(
            label = label,
            options = s.routes.keys(),
            # index = 0,     # not to be used, we set key instead
            key = key,       # default taken from session state
            on_change = cb,
            )

        # create widget
        if method == 'selectbox':
            position.selectbox(**kwargs)
        elif method == 'radio':
            position.radio(**kwargs)
        elif method == 'kwargs':
            # avoid creating widget, just return kwargs
            pass
        else:
            st.error('Invalid choosing method chosen')
        return kwargs


#