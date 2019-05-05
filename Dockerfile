FROM missxa/melodic-crystal-roboy

WORKDIR /RoboyImitator

RUN apt-get install build-essential libssl1.0.0 libasound2

# install roboy-intelligence-team
RUN pip3 install -r requirements.txt \
  & pip3 install -e .

ENTRYPOINT [ "scripts/entrypoint.sh" ]
