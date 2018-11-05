import boto3

region = 'us-east-1'

filters = [
    {
        'Name': 'instance-state-name',
        'Values': ['running', 'stopped']
    },
    {
        'Name': 'tag:Scheduled',
        'Values': ['true']
    }
]

def exec_action(instance, action):
    
    switcher = {
        'stop': instance.stop,
        'start': instance.start,
        'reboot': instance.reboot,
        'terminate': instance.terminate
    }
    
    function = switcher.get(action)
    return function()

def lambda_handler(event, context):
    
    action = event['action']
    
    filters.append(
        {
            'Name': 'tag:' + event['tag_key'],
            'Values': [event['tag_value']]
        }
    )
    
    try: 
        ec2 = boto3.resource('ec2', region_name=region)
        instances = ec2.instances.filter(Filters=filters)
        
        for instance in instances:
            print 'Trying to execute a ' + str(action) + ' in the instance ' +  str(instance)
            exec_action(instance, action)
    
    except ClientError as e:
        print(e)
