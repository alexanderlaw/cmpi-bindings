"""Python Provider for TestAtom

Instruments the CIM class TestAtom

"""

import pywbem
import sys
from pywbem.cim_provider2 import CIMProvider2

class TestAtomProvider(CIMProvider2):
    """Instrument the CIM class TestAtom 

    Model an atom, For use with CIMOM and PyWBEM Provider
    
    """
    def __init__ (self, env):
        logger = env.get_logger()
        logger.log_debug('Initializing provider %s from %s' \
                % (self.__class__.__name__, __file__))
        self.storage = {}



    def get_instance(self, env, model):
        """Return an instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstance to be returned.  The 
            key properties are set on this instance to correspond to the 
            instanceName that was requested.  The properties of the model
            are already filtered according to the PropertyList from the 
            request.  Only properties present in the model need to be
            given values.  If you prefer, you can set all of the 
            values, and the instance will be filtered for you. 
        cim_class -- The pywbem.CIMClass

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the CIM Class does exist, but the requested CIM 
            Instance does not exist in the specified namespace)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """
        
        logger = env.get_logger()
        logger.log_debug('Entering %s.get_instance()' \
                % self.__class__.__name__)
       
        try:
            #logger.log_debug("**** GET_INSTANCE model[name]: %s ****" % model['Name'])
            #print "**** GET_INSTANCE model[name]: %s ****" % str(model['Name'])
            #if model['Name'] in self.storage.keys():
            inst = self.storage[model['Name']]
            #else:
                #print "This is not working.... ******* FIX ME"

        except KeyError:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND)
        #print " **** Setting Model Properties: ****"
        for k, v in inst.properties.items():
            model[k] = v

        #return inst
        return model


    def enum_instances(self, env, model, keys_only):
        """Enumerate instances.

        The WBEM operations EnumerateInstances and EnumerateInstanceNames
        are both mapped to this method. 
        This method is a python generator

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstances to be generated.  
            The properties of the model are already filtered according to 
            the PropertyList from the request.  Only properties present in 
            the model need to be given values.  If you prefer, you can 
            always set all of the values, and the instance will be filtered 
            for you. 
        cim_class -- The pywbem.CIMClass
        keys_only -- A boolean.  True if only the key properties should be
            set on the generated instances.

        Possible Errors:
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.enum_instances()' \
                % self.__class__.__name__)
        #for atom in self.storage.keys():
            #print "Key = %s " %str(atom)

        ## Test context
        if not isinstance(env.ctx['CMPIInvocationFlags'], pywbem.Uint32):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 
                    'context is broken: ' + `env.ctx`)

        oldlen = len(env.ctx)
        env.ctx['foo'] = 'bar'
        if env.ctx['foo'] != 'bar':
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 
                    'context is broken: ' + `env.ctx`)

        if oldlen + 1 != len(env.ctx):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 
                    'context is broken: ' + `env.ctx`)

        if not 'foo' in env.ctx:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 
                    'context is broken: ' + `env.ctx`)

        if 'foobar' in env.ctx:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 
                    'context is broken: ' + `env.ctx`)

        env.ctx.update(foobar='foobar')
        if env.ctx['foobar'] != 'foobar':
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, 
                    'context is broken: ' + `env.ctx`)

        ## end context tests

        for key in self.storage.keys():
            #print "***** HELLO ***** "
            #logger.log_debug("************ ENUM_INSTANCES ********")
            #logger.log_debug(" **** model['Name'] = %s ****" % key)
            #print "************ ENUM_INSTANCES ********"
            #print " **** model['Name'] = %s ****" % key
            model['Name'] = key
            model.path['Name'] = key
            try:
                yield self.get_instance(env, model)
            except pywbem.CIMError, (num, msg):
                if num not in (pywbem.CIM_ERR_NOT_FOUND, 
                               pywbem.CIM_ERR_ACCESS_DENIED):
                    raise

    def set_instance(self, env, instance, modify_existing):
        """Return a newly created or modified instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance -- The new pywbem.CIMInstance.  If modifying an existing 
            instance, the properties on this instance have been filtered by 
            the PropertyList from the request.
        previous_instance -- The previous pywbem.CIMInstance if modifying 
            an existing instance.  None if creating a new instance. 
        cim_class -- The pywbem.CIMClass

        Return the new instance.  The keys must be set on the new instance. 

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_NOT_SUPPORTED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_ALREADY_EXISTS (the CIM Instance already exists -- only 
            valid if previous_instance is None, indicating that the operation
            was CreateInstance)
        CIM_ERR_NOT_FOUND (the CIM Instance does not exist -- only valid 
            if previous_instance is not None, indicating that the operation
            was ModifyInstance)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """

        logger = env.get_logger()
        logger.log_debug('Entering %s.set_instance()' \
                % self.__class__.__name__)

        if modify_existing:
            if instance['Name'] not in self.storage:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND)
            inst = self.storage[instance.path['Name']] 
            inst.properties.update(instance.properties)
            #logger.log_debug("***** Updating stuff :%s *****" % instance.properties)

        else:
            if instance.path['Name'] in self.storage:
                    raise pywbem.CIMError(pywbem.CIM_ERR_ALREADY_EXISTS)
            else:
                #Creating a new instance
                #print "Copying Instance"
                #print "Instance name: %s"%str(instance['Name'])
                #for key in instance.properties.keys():
                    #print "key=%s"%str(key)
                self.storage[instance.path['Name']] = instance.copy()

        instance.path['Name'] = instance['Name']
        return instance

    def delete_instance(self, env, instance_name):
        """Delete an instance.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        instance_name -- A pywbem.CIMInstanceName specifying the instance 
            to delete.

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_NOT_SUPPORTED
        CIM_ERR_INVALID_NAMESPACE
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate, unrecognized 
            or otherwise incorrect parameters)
        CIM_ERR_INVALID_CLASS (the CIM Class does not exist in the specified 
            namespace)
        CIM_ERR_NOT_FOUND (the CIM Class does exist, but the requested CIM 
            Instance does not exist in the specified namespace)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """ 
        logger = env.get_logger()
        logger.log_debug('Entering %s.delete_instance()' \
                % self.__class__.__name__)
        try:
            del self.storage[instance_name['Name']]
        except KeyError:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND)
        
## end of class TestAtomProvider

def get_providers(env): 
    testatom_prov = TestAtomProvider(env)  
    return {'Test_Atom': testatom_prov} 
