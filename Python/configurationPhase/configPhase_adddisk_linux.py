

configspec = morpheus['spec']
cDrive_size = configspec['volumes'][0]['size']
cDrive_bytes = configspec['volumes'][0]['sizeBytes']
cDrive_id = configspec['volumes'][0]['id']

# Check if additional disk is needed
if configspec['customOptions'].get('mountCount'):
  diskCount = configspec['customOptions']['mountCount']

  # Map disk count to number of disks
  disk_count_map = {
      "one": 1,
      "two": 2,
      "three": 3,
      "four": 4,
      "five": 5
  }

  displayNumber = len(configspec['volumes'])

  # Get the number of disks to add
  num_disks = disk_count_map.get(diskCount, 0)
  disk_id = cDrive_id

  # Add the specified number of disks from diskOne through diskN
  for i in range(num_disks):
      disk_id += 1
      disk_number = i + 1
      disk_name_map = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}
      disk_size_key = f"mount{disk_name_map[disk_number]}"
      disk_label_key = f"mount{disk_name_map[disk_number]}Label"
    
      disk_size = None
      disk_size_bytes = None
      if disk_size_key in configspec['customOptions']:
          try:
              disk_size = int(configspec['customOptions'][disk_size_key])
          except (ValueError, TypeError):
              disk_size = 10  # Default to 10GB if not a valid integer
      else:
          disk_size = 10  # Default to 10GB if not found
      disk_size_bytes = disk_size * 1024 * 1024 * 1024  # Convert GB to bytes

      # Use label from customOptions if present, otherwise fallback to default name
      disk_name = configspec['customOptions'].get(disk_label_key, f"disk{disk_name_map[disk_number]}")

      new_disk = {
          "id": disk_id,
          "size": disk_size,
          "name": disk_name,
          "sizeBytes": disk_size_bytes,
          "rootVolume": False,
          "storageType": configspec['volumes'][0]['storageType'],
          "datastoreId": configspec['volumes'][0]['datastoreId'],
          "displayOrder": displayNumber + i
      }
    
      configspec['volumes'].append(new_disk)

newspec = {}
newspec['spec'] = configspec
print(json.dumps(newspec))