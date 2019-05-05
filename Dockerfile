FROM missxa/melodic-crystal-roboy

#TODO libs

# install roboy-intelligence-team
RUN cd /RoboyImitator/
RUN pip3 install -r requirements.txt
RUN pip3 install -e .
