FROM  python:3

COPY . /tmp/fakelogs
RUN pip install /tmp/fakelogs && \
    rm -r /tmp/fakelogs

#RUN pip install fakelogs

ENV OUTPUT_FORMAT=json
ENV TIME_TO_SLEEP=1
ENV RECORDS_PER_ITERATION=10
ENV POOL_PROCESSES=2
ENV MAX_ITERATIONS=0

CMD ["python", "-c", "import fakelogs.cli ; fakelogs.cli.main()"]
