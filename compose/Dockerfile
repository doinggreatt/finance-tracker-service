FROM python:3.13-slim 

WORKDIR /app 

RUN apt update && apt install -y bash
ARG DEBUG_ARG

COPY requirements/base.txt . 
RUN pip install -r base.txt

COPY requirements/ ./requirements/
ENV DEBUG={$DEBUG_ARG}

RUN if [ "$DEBUG_ARG" = "true" ] ; then \
        pip install -r requirements/dev.txt --no-cache-dir ; \
    else \ 
        pip install -r requirements/prod.txt --no-cache-dir ; \ 
    fi



COPY . .   

RUN chmod +x compose/entrypoint.sh 

ENTRYPOINT [ "/bin/bash", "/app/compose/entrypoint.sh" ]