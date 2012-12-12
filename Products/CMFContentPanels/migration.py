import logging

logger = logging.getLogger("Products.CMFContentPanels")
PROFILE_ID = 'profile-Products.CMFContentPanels:default'

def run_types_step(context):
    context.runImportStepFromProfile(PROFILE_ID, 'typeinfo')
