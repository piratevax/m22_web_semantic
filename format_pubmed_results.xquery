xquery version "3.1";

let $articles :=doc("/db/pubmed/pubmed_result.xml")/*

for $article in $articles/PubmedArticle
return
    <Corpus>
        <Article>
            <Title>
                {$article/MedlineCitation/Article/ArticleTitle/text()}
            </Title>
            <MeshTerms>
                {
                    for $mesh_heading in $article/MedlineCitation/MeshHeadingList/MeshHeading
                    return
                        if ($mesh_heading/DescriptorName and $mesh_heading/QualifierName)
                        then
                        $mesh_heading
                        else
                        <MeshHeading>
                            {
                            $mesh_heading/DescriptorName
                            }
                            <QualifierName UI="NA" MajorTopicYN="NA">NA</QualifierName>
                        </MeshHeading>
                }
            </MeshTerms>
        </Article>
    </Corpus>
