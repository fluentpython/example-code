# Use an official Python runtime as a base image
FROM centos

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

#Unzip flag files
RUN yum install -y unzip
RUN unzip flags.zip

#Install nginx
RUN yum install -y epel-release
RUN yum install -y nginx

#Setup Nginx
RUN mv -f nginx.conf /etc/nginx/nginx.conf

#Install vaurien
RUN yum install -y centos-release-scl gcc zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel python-devel python-pip
RUN pip install vaurien







# Install any needed packages specified in requirements.txt
#RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
#EXPOSE 80

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
#CMD ["python", "app.py"]
