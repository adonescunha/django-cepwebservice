# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Estado'
        db.create_table('cepwebservice_estado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uf', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('nome', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('cepwebservice', ['Estado'])

        # Adding model 'Cidade'
        db.create_table('cepwebservice_cidade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cepwebservice.Estado'])),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cepwebservice', ['Cidade'])

        # Adding unique constraint on 'Cidade', fields ['estado', 'nome']
        db.create_unique('cepwebservice_cidade', ['estado_id', 'nome'])

        # Adding model 'Bairro'
        db.create_table('cepwebservice_bairro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cidade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cepwebservice.Cidade'])),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cepwebservice', ['Bairro'])

        # Adding unique constraint on 'Bairro', fields ['cidade', 'nome']
        db.create_unique('cepwebservice_bairro', ['cidade_id', 'nome'])

        # Adding model 'Logradouro'
        db.create_table('cepwebservice_logradouro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bairro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cepwebservice.Bairro'])),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('cepwebservice', ['Logradouro'])

        # Adding unique constraint on 'Logradouro', fields ['bairro', 'nome', 'tipo']
        db.create_unique('cepwebservice_logradouro', ['bairro_id', 'nome', 'tipo'])

        # Adding model 'CEP'
        db.create_table('cepwebservice_cep', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('logradouro', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cepwebservice.Logradouro'])),
            ('cep', self.gf('django.db.models.fields.CharField')(unique=True, max_length=9)),
        ))
        db.send_create_signal('cepwebservice', ['CEP'])


    def backwards(self, orm):
        # Removing unique constraint on 'Logradouro', fields ['bairro', 'nome', 'tipo']
        db.delete_unique('cepwebservice_logradouro', ['bairro_id', 'nome', 'tipo'])

        # Removing unique constraint on 'Bairro', fields ['cidade', 'nome']
        db.delete_unique('cepwebservice_bairro', ['cidade_id', 'nome'])

        # Removing unique constraint on 'Cidade', fields ['estado', 'nome']
        db.delete_unique('cepwebservice_cidade', ['estado_id', 'nome'])

        # Deleting model 'Estado'
        db.delete_table('cepwebservice_estado')

        # Deleting model 'Cidade'
        db.delete_table('cepwebservice_cidade')

        # Deleting model 'Bairro'
        db.delete_table('cepwebservice_bairro')

        # Deleting model 'Logradouro'
        db.delete_table('cepwebservice_logradouro')

        # Deleting model 'CEP'
        db.delete_table('cepwebservice_cep')


    models = {
        'cepwebservice.bairro': {
            'Meta': {'ordering': "('nome',)", 'unique_together': "(('cidade', 'nome'),)", 'object_name': 'Bairro'},
            'cidade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cepwebservice.Cidade']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cepwebservice.cep': {
            'Meta': {'object_name': 'CEP'},
            'cep': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logradouro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cepwebservice.Logradouro']"})
        },
        'cepwebservice.cidade': {
            'Meta': {'ordering': "('nome',)", 'unique_together': "(('estado', 'nome'),)", 'object_name': 'Cidade'},
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cepwebservice.Estado']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cepwebservice.estado': {
            'Meta': {'ordering': "('nome',)", 'object_name': 'Estado'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'uf': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'})
        },
        'cepwebservice.logradouro': {
            'Meta': {'ordering': "('nome',)", 'unique_together': "(('bairro', 'nome', 'tipo'),)", 'object_name': 'Logradouro'},
            'bairro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cepwebservice.Bairro']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['cepwebservice']