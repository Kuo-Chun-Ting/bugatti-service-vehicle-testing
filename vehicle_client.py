from tornado.httpclient import AsyncHTTPClient
from config import auth_user, auth_entry_point, vehicle_entry_point
from functools import wraps
from decorator import exception_handler
import asyncio
import json
import uuid


class VehicleClient:
    def __init__(self):
        self.entry_point = vehicle_entry_point
        self.headers = {'accept':'application/json',
                        'Authorization': None,
                        'Content-Type': 'application/json'}
        self.http_client = AsyncHTTPClient()

    async def get_token(self):
        """Get the access token from Alpha."""

        try:
            api_endpoint = auth_entry_point

            headers = {'X-TCLOUD-SERVICE': 'fm',
                        'Content-Type': 'application/json'}

            body = json.dumps(auth_user)

            response = await self.http_client.fetch(api_endpoint,
                                            raise_error=False,
                                            method='POST',
                                            body=body,
                                            headers=headers)
            if response.error is None:
                token = f"Bearer {json.loads(response.body)['msg']['v3']['access_token']}"
                self.headers['Authorization'] = token
                print(f'Getting token successful.')
            else:
                print(f'Getting token failed.')

        except Exception as e:
            print(f'An error occurred while getting token {e}')

    async def auth_promise_fetch(self, fetch):
        response = await fetch()
        if response.code in (401, 599):
                await self.get_token()
                return await fetch()
        return response
    
    @exception_handler
    async def post_route(self, name):
        """Create a route and return the created id."""
        
        api_endpoint = f'{self.entry_point}route'
        body = json.dumps({"name": name})
        method = 'POST'
        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method=method,
                                        body=body,
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def put_route(self, id, name):
        """Modify a route by the given id."""

        api_endpoint = f'{self.entry_point}route?id={id}'
        body = json.dumps({"name": name})

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                            raise_error=False,
                                            method='PUT',
                                            body=body,
                                            headers=self.headers)
        return await self.auth_promise_fetch(fetch)
    
    @exception_handler
    async def get_route_list(self, id=None)-> list:
        """List routes by default filter."""

        api_endpoint = f'{self.entry_point}route/list?org_name=lileesystems&offset=0&count=10000'
        if id is not None:
            api_endpoint += f'&search_id={id}'
        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                            raise_error=False,
                                            method='GET',
                                            headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def delete_route(self, id):
        """Delte a route by the given id."""

        api_endpoint = f'{self.entry_point}route?id={id}'
        
        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='DELETE',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)               
        
    @exception_handler
    async def post_driver(self, name)-> str:
        """Create a driver and return the created id."""

        api_endpoint = f'{self.entry_point}driver'
        body = json.dumps({"name": name})

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='POST',
                                        body=body,
                                        headers=self.headers)

        return await self.auth_promise_fetch(fetch) 

    @exception_handler
    async def put_driver(self, id, name):
        """Modify a driver by the given id."""

        api_endpoint = f'{self.entry_point}driver?id={id}'
        body = json.dumps({"name": name})

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='PUT',
                                        body=body,
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch) 

    @exception_handler
    async def get_driver_list(self, id=None)-> list:
        """List drivers by default filter."""

        api_endpoint = f'{self.entry_point}driver/list?org_name=lileesystems&offset=0&count=10000'
        if id is not None:
            api_endpoint += f'&search_id={id}'
        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='GET',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def delete_driver(self, id):
        """Delte a driver by the given id."""

        api_endpoint = f'{self.entry_point}driver?id={id}'

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='DELETE',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def post_program(self, name)-> str:
        """Create a program and return the created id."""

        api_endpoint = f'{self.entry_point}program'
        body = json.dumps({"name": name,
                            "description": "Test program",
                            "manager": "John"})
        
        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='POST',
                                        body=body,
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def put_program(self, id, name):
        """Modify a program by the given id."""

        api_endpoint = f'{self.entry_point}program?id={id}'
        body = json.dumps({"name": name,
                            "description": "Test program1000",
                            "manager": "John"})

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='PUT',
                                        body=body,
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def get_program(self, id)->object:
        """Get a program by the given id."""

        api_endpoint = f'{self.entry_point}program?org_name=lileesystems&id={id}'\
                        '&with_children_count=false&with_vehicle_count=false&with_full_path=false'

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='GET',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def get_program_search(self, id)->list:
        """Get a program by the given id."""

        api_endpoint = f'{self.entry_point}program/search?org_name=lileesystems&id={id}'

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='GET',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def get_program_list(self, id=None)-> list:
        """List programs by default filter."""

        api_endpoint = f'{self.entry_point}program/list?org_name=lileesystems&with_children_count=false'\
                        '&with_vehicle_count=false&with_full_path=false&with_top=false'
        if id is not None:
            api_endpoint += f'&search_id={id}'
        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='GET',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def delete_program(self, id):
        """Delte a program by the given id."""

        api_endpoint = f'{self.entry_point}program?id={id}'

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='DELETE',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def post_item(self, name)-> (str, str):
        """Create a vehicle and return the created id and device id."""

        api_endpoint = f'{self.entry_point}item'
        body = json.dumps({"driver_id": None,
                            "route_id": None,
                            "device_mac": "lillardmac12345",
                            "name": name,
                            "note": "test note",
                            "kind": None,
                            "capacity": 4})

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='POST',
                                        body=body,
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def get_list(self, id=None, program_id=None)-> list:
        """List vehicles by default filter."""

        api_endpoint = f'{self.entry_point}list?org_name=lileesystems'\
                        '&with_program_info=false&with_program_path=false'\
                        '&with_device_info=false&without_no_device=false'\
                        '&offset=0&count=1000'
        if program_id != None:
            api_endpoint += f'&program_id={program_id}'
        
        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='GET',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def get_list_by_device(self, device_ids)-> list:
        """List vehicles by default filter."""

        api_endpoint = f'{self.entry_point}list/by_device?org_name=lileesystems&device_ids={device_ids}&with_program_info=false&with_full_path=false&with_device_info=false'

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='GET',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def put_program_link(self, id, program_id):
        """Link between a program and some vehicles."""
        
        api_endpoint = f'{self.entry_point}program/link?id={id}'
        modified_name = 'script test modified'
        body = json.dumps({"program_id": program_id,
                            "vehicle_ids": [id]})

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='PUT',
                                        body=body,
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def put_item(self, vehicle_id, device_mac, name):
        """Modify a vehicle by the given id."""

        api_endpoint = f'{self.entry_point}item?id={vehicle_id}'
        body = json.dumps({"driver_id": None,
                            "route_id": None,
                            "device_mac": device_mac,
                            "name": name,
                            "note": "test note 222",
                            "kind": None,
                            "capacity": 22})

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='PUT',
                                        body=body,
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def delete_item(self, id):
        """Delte a vehicle by the given id."""

        api_endpoint = f'{self.entry_point}item?id={id}'

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='DELETE',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def get_device_list(self, id=None)-> list:
        """List devices by default filter."""

        api_endpoint = f'{self.entry_point}device/list?org_name=lileesystems&offset=0&count=1000'

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='GET',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def get_event_list(self, start, end)->list:
        """List event list by default filter."""

        api_endpoint = f'{self.entry_point}event/list?start_time={start}&end_time={end}'

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='GET',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def get_telematic(self)->object:
        """Get telematic by default filter."""

        api_endpoint = f'{self.entry_point}telematic?id=d9144f8d-3e0f-4df6-9a89-92aa7c0d36b8'\
                        '&start_time=1585440000&end_time=1585499424&chart_granularity=86400'\
                        '&map_granularity=86400'

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='GET',
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)

    @exception_handler
    async def post_realtime(self)->object:
        """Get real-time data by a default vehicle."""

        api_endpoint = f'{self.entry_point}realtime'
        body = json.dumps({"vehicle_ids": [
                            "d9144f8d-3e0f-4df6-9a89-92aa7c0d36b8"
                            ],
                            "fields": ["vin",
                                        "is_engine_light_on",
                                        "device_status",
                                        "camera_info"]})

        async def fetch():
            return await self.http_client.fetch(api_endpoint,
                                        raise_error=False,
                                        method='POST',
                                        body=body,
                                        headers=self.headers)
        return await self.auth_promise_fetch(fetch)
    

