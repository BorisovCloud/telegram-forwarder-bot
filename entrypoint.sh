#!/bin/bash

# Define mount point and create mount point directory
MOUNT_POINT="/app/session_data"
mkdir -p ${MOUNT_POINT}

# Mount the Azure File Share
mount -t cifs //${STORAGE_ACCOUNT_NAME}.file.core.windows.net/${FILE_SHARE_NAME} ${MOUNT_POINT} -o vers=3.0,username=${STORAGE_ACCOUNT_NAME},password=${STORAGE_ACCOUNT_KEY},dir_mode=0777,file_mode=0777,serverino

# Check if the mount was successful
if mountpoint -q ${MOUNT_POINT}; then
    echo "Azure File Share mounted successfully at ${MOUNT_POINT}"
else
    echo "Failed to mount Azure File Share"
    exit 1
fi

# Run the main application (replace 'your_script.py' with your actual app)
exec python -u /app/app.py