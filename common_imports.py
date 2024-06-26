from flask import Flask, request, jsonify, session, redirect, url_for, flash, send_file
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os
import uuid
import datetime
import random
import copy
import ssl
import cv2 as cv
from PIL import Image
import numpy as np
import dlib
import tensorflow as tf
from keras_facenet import FaceNet
import csv
import pickle
from io import BytesIO
import json
import matplotlib.pyplot as plt
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
import requests
import mysql.connector
from mysql.connector import errorcode

