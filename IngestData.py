import os
import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

from google.cloud import bigquery
bq = bigquery.Client()

parser = argparse.ArgumentParser()

options = PipelineOptions(flags=argv)

argv = ['--project=project',
        '--job_name=mytestjob',
        '--runner=DataflowRunner',
        '--max_num_workers=10',
        '--region=us-central1',
        '--temp_location=gs://project/staging/',
        '--staging_location=gs://project/staging/',
        ]

# Argumentos para o job
parser.add_argument('--output_price',
                    default='DATASET.PRICE_QUOTE')

parser.add_argument('--output_material',
                    default='DATASET.BILL_MATERIAL')

parser.add_argument('--output_component',
                    default='DATASET.COMPONENT_BOSS')

parser.add_argument('--input',
                    default='gs://project/stage_mis/Josimar/MACHINES/PRICE_QUOTE.csv')

parser.add_argument('--input_material',
                    default='gs://project/stage_mis/Josimar/MACHINES/BILL_MATERIAL.csv')

parser.add_argument('--in_component',
                    default='gs://project/stage_mis/Josimar/MACHINES/COMPONENT_BOSS.csv')

known_args, pipeline_args = parser.parse_known_args(argv)




def split_price(input):
    lista = input.split(',')
    row = dict(zip(('tube_assembly_id','supplier','quote_date','annual_usage','min_order_quantity','bracket_pricing','quantity','cost'),lista))
    return row

def split_material(input):
    lista = input.split(',')
    row = dict(zip(('tube_assembly_id','component_id_1','quantity_1','component_id_2','quantity_2'
                                      ,'component_id_3','quantity_3','component_id_4','quantity_4'
                                      ,'component_id_5','quantity_5','component_id_6','quantity_6'
                                      ,'component_id_7','quantity_7','component_id_8','quantity_8'),lista))
    return row

def split_component(input):
    lista = input.split(',')
    row = dict(zip(('component_id','component_type_id','type','connection_type_id','outside_shape','base_type','height_over_tube'
                    ,'bolt_pattern_long','bolt_pattern_wide','groove','base_diameter','shoulder_diameter','unique_feature','orientation'
                    ,'weight'),lista))
    return row

bq_source = beam.io.BigQuerySource(query='query_normatiza_price_quote', use_standard_sql=True)

with beam.Pipeline(argv=argv) as p:
    
# O dataflow já resolve a questão da data, ajustando automaticamente    
    read_price_quote_from_csv = (
    p
    | 'Read Price File'  >> beam.io.ReadFromText(known_args.input,skip_header_lines=1)
    | 'Split Price File' >> beam.Map(split_price)
    | 'Load Price Table' >> beam.io.WriteToBigQuery(known_args.output_price,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        schema="""tube_assembly_id:STRING,supplier:STRING,quote_date:STRING,annual_usage:STRING
                                 ,min_order_quantity:STRING,bracket_pricing:STRING,quantity:STRING,cost:STRING """)
)
    
    read_bill_material_from_csv = (
    p
    | 'Read Material File'  >> beam.io.ReadFromText(known_args.input_material,skip_header_lines=1)
    | 'Split Material File' >> beam.Map(split_material)
    | 'Load Material Table' >> beam.io.WriteToBigQuery(known_args.output_material,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        schema="""tube_assembly_id:STRING,component_id_1:STRING,quantity_1:STRING,component_id_2:STRING,quantity_2:STRING
                                                         ,component_id_3:STRING,quantity_3:STRING,component_id_4:STRING,quantity_4:STRING
                                                         ,component_id_5:STRING,quantity_5:STRING,component_id_6:STRING,quantity_6:STRING
                                                         ,component_id_7:STRING,quantity_7:STRING,component_id_8:STRING,quantity_8:STRING """)
)
    
    read_component_from_csv = (
    p
    | 'Read Component File'  >> beam.io.ReadFromText(known_args.in_component,skip_header_lines=1)
    | 'Split Component File' >> beam.Map(split_component)
    | 'Load Component table' >> beam.io.WriteToBigQuery(known_args.output_component,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                        schema="""component_id:STRING,component_type_id:STRING,type:STRING,connection_type_id:STRING,outside_shape:STRING
                                 ,base_type:STRING,height_over_tube:STRING,bolt_pattern_long:STRING,bolt_pattern_wide:STRING,groove:STRING
                                 ,base_diameter:STRING,shoulder_diameter:STRING,unique_feature:STRING,orientation:STRING,weight:STRING """)                              
)

    
run()
