FROM freqtradeorg/freqtrade:stable

# Switch user to root if you must install something from apt
# Don't forget to switch the user back below!
# USER root

# The below dependency - pyti - serves as an example. Please use whatever you need!
RUN pip install --user ta

# USER ftuser