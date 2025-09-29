
import sys
import os
import pytest
from flask import Flask
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from edge.controller import EdgeController

def test_edge_controller_get_load(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'test')
    e = EdgeController('http://localhost:5001')
    client = e.app.test_client()
    headers = {'Authorization': 'Bearer test'}
    resp = client.get('/get_load', headers=headers)
    assert resp.status_code == 200
    assert 'load' in resp.json

def test_edge_controller_get_load_unauthorized():
    e = EdgeController('http://localhost:5001')
    client = e.app.test_client()
    resp = client.get('/get_load')
    assert resp.status_code == 401

def test_edge_controller_health():
    e = EdgeController('http://localhost:5001')
    client = e.app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json['status'] == 'ok'
