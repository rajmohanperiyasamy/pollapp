#!/usr/bin/env python
# -*- coding: utf-8 -*-
from payments.paypal.standard.forms import PayPalStandardBaseForm
from payments.paypal.standard.pdt.models import PayPalPDT


class PayPalPDTForm(PayPalStandardBaseForm):
    class Meta:
        model = PayPalPDT