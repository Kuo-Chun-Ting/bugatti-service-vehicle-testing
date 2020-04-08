from vehicle_client import VehicleClient
from termcolor import colored
from functools import wraps
from decorator import clear, exception_handler
import asyncio
import uuid
import json


class VehicleTestBase:
    def __init__(self):
        self.client = VehicleClient()
        self.color_successful = colored("successful", "green")
        self.color_failed = colored("failed", "red")
        self.color_post = colored("POST", "green")
        self.color_put = colored("PUT", "yellow")
        self.color_delete = colored("DELETE", "red")
        self.color_get = colored("GET", "blue")
        self.test_name = 'script test'
        self.title = 'Default'

    def get_random_name(self):
        return f'{self.test_name} {uuid.uuid4()}'

    def get_msg(self, response):
        url = response.request.url
        method = response.request.method
        code = response.code
        if not response.error:
            print(f'{method} {url} {code}')
            return json.loads(response.body)['msg']
        print(f'{method} {url} {code}')


class RouteTest(VehicleTestBase):
    def __init__(self):
        super().__init__()
        self.title = 'Route'
        print(f'[{self.title}]')

    async def _post_route(self)->str:
        response = await self.client.post_route(self.test_name)
        id = self.get_msg(response)['id']
        return id
    
    async def _get_route_list(self, id=None)->list:
        response = await self.client.get_route_list(id)
        items = self.get_msg(response)['items']
        return items
    
    @exception_handler
    @clear
    async def clear(self):
        """Remove all the data created by this script."""
        
        items = await self._get_route_list()
        for item in items:
            if item['name'].startswith(self.test_name):
                await self.client.delete_route(item['id'])
    
    @exception_handler
    async def test_all(self):
        await self.test_post_route()
        await self.test_get_route_list()
        await self.test_put_route()
        await self.test_delete_route()
        await self.clear()
    
    @exception_handler
    async def test_post_route(self):
        id = await self._post_route()
        items = await self._get_route_list(id)
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_post}/route {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_post}/route {self.color_failed}')

    @exception_handler
    async def test_get_route_list(self):
        id = await self._post_route()
        items = await self._get_route_list(id)
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_get}/route/list {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/route/list {self.color_failed}')
    
    @exception_handler   
    async def test_put_route(self):
        id = await self._post_route()
        
        modified_name = self.get_random_name()
        await self.client.put_route(id, modified_name)

        items = await self._get_route_list(id)
        if any(x['name']==modified_name for x in items):
            print(f'[{self.title}]{self.color_put}/route {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_put}/route {self.color_failed}')

    @exception_handler
    async def test_delete_route(self):
        id = await self._post_route()
        
        await self.client.delete_route(id)

        items = await self._get_route_list(id)
        if not items:
            print(f'[{self.title}]{self.color_delete}/route {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_delete}/route {self.color_failed}')   


class DriverTest(VehicleTestBase):
    def __init__(self):
        super().__init__()
        self.title = 'Driver'
        print(f'[{self.title}]')

    async def _post_driver(self)->str:
        response = await self.client.post_driver(self.test_name)
        id = self.get_msg(response)['id']
        return id
    
    async def _get_driver_list(self, id=None)->list:
        response = await self.client.get_driver_list(id)
        items = self.get_msg(response)['items']
        return items
    
    @exception_handler
    @clear
    async def clear(self):
        """Remove all the data created by this script."""

        items = await self._get_driver_list()
        for item in items:
            if item['name'].startswith('script test'):
                await self.client.delete_driver(item['id'])

    @exception_handler
    async def test_all(self):
        await self.test_post_driver()
        await self.test_get_driver_list()
        await self.test_put_driver()
        await self.test_delete_driver()
        await self.clear()

    @exception_handler
    async def test_post_driver(self):
        id = await self._post_driver()

        items = await self._get_driver_list()
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_post}/driver {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_post}/driver {self.color_failed}')

    @exception_handler
    async def test_get_driver_list(self):
        id = await self._post_driver()

        items = await self._get_driver_list()
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_get}/driver/list {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/driver/list {self.color_failed}')
  
    @exception_handler  
    async def test_put_driver(self):
        id = await self._post_driver()

        modified_name = self.get_random_name()
        await self.client.put_driver(id, modified_name)

        items = await self._get_driver_list()
        if any(x['name']==modified_name for x in items):
            print(f'[{self.title}]{self.color_put}/driver {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_put}/driver {self.color_failed}')

    @exception_handler
    async def test_delete_driver(self):
        id = await self._post_driver()
        
        await self.client.delete_driver(id)

        items = await self._get_driver_list(id)
        if not items:
            print(f'[{self.title}]{self.color_delete}/driver {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_delete}/driver {self.color_failed}')   


class DeviceTest(VehicleTestBase):
    def __init__(self):
        super().__init__()
        self.title = 'Device'
        print(f'[{self.title}]')

    async def _get_device_list(self, id=None)->list:
        response = await self.client.get_device_list(id)
        items = self.get_msg(response)['items']
        return items

    @exception_handler
    async def test_all(self):
        await self.test_get_device_list()

    @exception_handler
    async def test_get_device_list(self):
        items = await self._get_device_list()
        if items != None:
            print(f'[{self.title}]{self.color_get}/device/list {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/device/list {self.color_failed}')


class ProgramTest(VehicleTestBase):
    def __init__(self):
        super().__init__()
        self.title = 'Program'
        print(f'[{self.title}]')

    async def _post_program(self)->str:
        response = await self.client.post_program(self.get_random_name())
        id = self.get_msg(response)['id']
        return id
  
    async def _get_program_list(self, id=None)->list:
        response = await self.client.get_program_list(id)
        programs = self.get_msg(response)
        return programs

    @exception_handler
    @clear
    async def clear(self):
        """Remove all the data created by this script."""

        items = await self._get_program_list()
        for item in items:
            if item['name'].startswith('script test'):
                await self.client.delete_program(item['id'])

    @exception_handler
    async def test_all(self):
        await self.test_post_program()
        await self.test_get_program()
        await self.test_get_program_list()
        await self.test_get_program_search()
        await self.test_put_program()
        await self.test_delete_program()
        await self.clear()

    @exception_handler
    async def test_post_program(self):
        id = await self._post_program()

        items = await self._get_program_list(id)
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_post}/program {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_post}/program {self.color_failed}')

    @exception_handler
    async def test_get_program(self):
        id = await self._post_program()

        response = await self.client.get_program(id)
        item = self.get_msg(response)
        if item['id']==id:
            print(f'[{self.title}]{self.color_get}/program {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/program {self.color_failed}')
    
    @exception_handler
    async def test_get_program_list(self):
        id = await self._post_program()

        items = await self._get_program_list(id)
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_get}/program/list {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/program/list {self.color_failed}')
    
    @exception_handler
    async def test_get_program_search(self):
        id = await self._post_program()

        response = await self.client.get_program_search(id)
        items = self.get_msg(response)
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_get}/program/search {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/program/search {self.color_failed}')
    
    @exception_handler
    async def test_put_program(self):
        id = await self._post_program()

        modified_name = self.get_random_name()
        await self.client.put_program(id, modified_name)

        items = await self._get_program_list(id)
        if any(x['name']==modified_name for x in items):
            print(f'[{self.title}]{self.color_put}/program {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_put}/program {self.color_failed}')

    @exception_handler
    async def test_delete_program(self):
        id = await self._post_program()
        
        await self.client.delete_program(id)

        items = await self._get_program_list(id)
        if any(x['id']!=id for x in items):
            print(f'[{self.title}]{self.color_delete}/program {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_delete}/program {self.color_failed}')   
    

class VehicleTest(VehicleTestBase):
    def __init__(self):
        super().__init__()
        self.title = 'Vehicle'
        print(f'[{self.title}]')

    async def _post_item(self)->str:
        response = await self.client.post_item(self.test_name)
        msg = self.get_msg(response)
        return msg['id'], msg['device_mac']
    
    async def _get_list(self, id=None)->list:
        response = await self.client.get_list(id)
        items = self.get_msg(response)['items']
        return items
     
    @exception_handler 
    @clear
    async def clear(self):
        """Remove all the data created by this script."""

        items = await self._get_list()
        for item in items:
            if item['name'].startswith('script test'):
                await self.client.delete_item(item['id'])
     
    @exception_handler
    async def test_all(self):
        await self.test_post_item()
        await self.test_get_list()
        await self.test_get_list_by_device()
        await self.test_put_item()
        await self.test_put_program_link()
        await self.test_delete_item()
        await self.clear()

    @exception_handler
    async def test_post_item(self):
        id, device_id = await self._post_item()

        items = await self._get_list(id)
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_post}/item {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_post}/item {self.color_failed}')

    @exception_handler
    async def test_get_list(self):
        id, device_id = await self._post_item()

        items = await self._get_list(id)
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_get}/item {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/item {self.color_failed}')

    @exception_handler
    async def test_get_list_by_device(self):
        id, device_id = await self._post_item()

        response = await self.client.get_list_by_device(device_id)
        items = self.get_msg(response)['lileesystems']
        if any(x['id']==id for x in items):
            print(f'[{self.title}]{self.color_get}/list/by_device {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/list/by_device {self.color_failed}')

    @exception_handler
    async def test_put_item(self):
        id, device_id = await self._post_item()

        modified_name = self.get_random_name()
        await self.client.put_item(id, device_id, modified_name)

        items = await self._get_list(id)
        if any(x['name']==modified_name for x in items):
            print(f'[{self.title}]{self.color_put}/item {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_put}/item {self.color_failed}')

    @exception_handler
    async def test_delete_item(self):
        id, device_id = await self._post_item()
        
        await self.client.delete_item(id)

        items = await self._get_list(id)
        if any(x['id']!=id for x in items):
            print(f'[{self.title}]{self.color_delete}/item {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_delete}/item {self.color_failed}')   

    @exception_handler
    async def test_put_program_link(self):
        response = await self.client.post_program(self.get_random_name())
        program_id = self.get_msg(response)['id']
        vehicle_id, device_id = await self._post_item()

        await self.client.put_program_link(vehicle_id, program_id)

        response = await self.client.get_list(program_id=program_id)
        items = self.get_msg(response)['items']
        if any(x['id']==vehicle_id for x in items):
            print(f'[{self.title}]{self.color_put}/program/link {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_put}/program/link {self.color_failed}')


class EventTest(VehicleTestBase):
    def __init__(self):
        super().__init__()
        self.title = 'Event'
        print(f'[{self.title}]')

    @exception_handler
    async def test_all(self):
        await self.test_get_event_list()

    @exception_handler
    async def test_get_event_list(self):
        response = await self.client.get_event_list(start = '1585149293',end = '1585149293000')
        items = self.get_msg(response)['list']
        if items:
            print(f'[{self.title}]{self.color_get}/event/list {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/event/list {self.color_failed}')
        

class TelematicTest(VehicleTestBase):
    def __init__(self):
        super().__init__()
        self.title = 'Telematic'
        print(f'[{self.title}]')

    @exception_handler
    async def test_all(self):
        await self.test_get_telematic()

    @exception_handler
    async def test_get_telematic(self):
        response = await self.client.get_telematic()
        item = self.get_msg(response)
        if item:
            print(f'[{self.title}]{self.color_get}/telematic {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_get}/telematic {self.color_failed}')


class RealtimeTest(VehicleTestBase):
    def __init__(self):
        super().__init__()
        self.title = 'Realtime'
        print(f'[{self.title}]')

    @exception_handler
    async def test_all(self):
        await self.test_post_realtime()

    @exception_handler
    async def test_post_realtime(self):
        response = await self.client.post_realtime()
        item = self.get_msg(response)
        if item:
            print(f'[{self.title}]{self.color_post}/realtime {self.color_successful}')
            return
        print(f'[{self.title}]{self.color_post}/realtime {self.color_failed}')


async def main():
    print('The test of the vehicle APIs is starting...')

    try:
        # await RouteTest().test_all()
        # await DriverTest().test_all()
        # await DeviceTest().test_all()
        # await ProgramTest().test_all()
        # await VehicleTest().test_all()
        await EventTest().test_all()
        await TelematicTest().test_all()
        await RealtimeTest().test_all()
    except Exception as e:
        print(f'An exceptional error ocurred in main. {e}')

    print('The test ends.')

