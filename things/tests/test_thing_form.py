from django.test import TestCase
from django import forms

from things.forms import ThingForm


# Create your tests here.
class ThingFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
            'name': 'Pen',
            'description': 'A tool that imprints ink on surface',
            'quantity': 12
        }

    # test valid form
    def test_for_valid_form(self):
        form = ThingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # form has necessary fields
    def test_form_has_necessary_fields(self):
        form = ThingForm(data=self.form_input)
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        description_widget = form.fields['description'].widget
        self.assertTrue(isinstance(description_widget, forms.Textarea))
        self.assertIn('quantity', form.fields)
        quantity_widget = form.fields['quantity'].widget
        self.assertTrue(isinstance(quantity_widget, forms.NumberInput))

    # test the form uses model validation
    def test_name_must_be_35_characters(self):
        self.form_input['name'] = "a" * 36
        form = ThingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_description_must_be_120_characters(self):
        self.form_input['description'] = "a" * 121
        form = ThingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_description_can_be_blank(self):
        self.form_input['description'] = ''
        form = ThingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_quantity_must_be_less_than_50(self):
        self.form_input['quantity'] = 51
        form = ThingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_name_must_be_greater_than_0(self):
        self.form_input['quantity'] = -1
        form = ThingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
