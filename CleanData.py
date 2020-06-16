f = open('/home/jupyter/Josimar/query_normatiza_price_quote.txt', "r")
query_price = f.read()

f = open('/home/jupyter/Josimar/query_normatiza_bill_material.txt', "r")
query_material = f.read()

f = open('/home/jupyter/Josimar/query_normatiza_component.txt', "r")
query_component = f.read()

bq_source_price = beam.io.BigQuerySource(query=query_price, use_standard_sql=True)
bq_source_material = beam.io.BigQuerySource(query=query_material, use_standard_sql=True)
bq_source_component = beam.io.BigQuerySource(query=query_component, use_standard_sql=True)


with beam.Pipeline(argv=argv) as p:
    
    read_price_quote_from_bq = (
    p
	| 'Query Price BQ' >> beam.io.Read(bq_source_price)
	| 'Write Price BQ' >> beam.io.WriteToBigQuery('DATASET.TB_PRICE_QUOTE',
                        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
)
    
    read_bill_material_from_bq = (
    p
	| 'Query Material BQ' >> beam.io.Read(bq_source_material)
	| 'Write Material BQ' >> beam.io.WriteToBigQuery('DATASET.TB_BILL_MATERIAL',
                          write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                          create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
) 
    
    read_component_from_bq = (
    p
	| 'Query Component BQ' >> beam.io.Read(bq_source_component)
	| 'Write Component BQ' >> beam.io.WriteToBigQuery('DATASET.TB_COMPONENT_BOSS',
                        write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
)       

run()
