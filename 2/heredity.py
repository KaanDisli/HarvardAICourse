import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                print(f'this is the joint porbability: {joint_probability(people, one_gene, two_genes, have_trait)}')
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    if one_gene == {"Harry"} and two_genes == {"James"} and have_trait == {"James"}:
        
    probabilities2=  []
 
    for person in people:
        if people[person]['father'] == None:
            if person in one_gene: # 0.03
                
                if person in have_trait: # 0.56
                    probabilities2.append(0.03 * 0.56)
                else:
                    probabilities2.append(0.03 * 0.44)
            elif person in two_genes: #0.01
                if person in have_trait: #0.65
                    probabilities2.append(0.01*0.65)
                else: #0.35
                    probabilities2.append(0.01*0.35)
            else: #0.96
                if person in have_trait: 
                    probabilities2.append(0.96*0.01)
                else:
                    probabilities2.append(0.96*0.99)
        else:
            current_father = people[person]['father']
            current_mother = people[person]['mother']
            probability_of_passing_gene = []
            if current_father in one_gene:
                probability_of_passing_gene.append(0.5) #BURAYA TEKRAR BAK SAYILARA
            elif current_father in two_genes:
                probability_of_passing_gene.append(0.99)
            else:
                probability_of_passing_gene.append(0.01)
                
            if current_mother in one_gene:
                probability_of_passing_gene.append(0.5)
            elif current_mother in two_genes:
                probability_of_passing_gene.append(0.99)
            else:
                probability_of_passing_gene.append(0.01)
            #------------------------------------------
            if person in one_gene:
                tempprob = ( (1-probability_of_passing_gene[0])*(probability_of_passing_gene[1]) ) + ((probability_of_passing_gene[0])*(1-probability_of_passing_gene[1]) )
                
                if person in have_trait:
                    probabilities2.append(PROBS["trait"][1][True]*tempprob)
                else:
                     probabilities2.append(PROBS["trait"][1][False]*tempprob)   
             
            elif person in two_genes:
                tempprob = probability_of_passing_gene[0]*probability_of_passing_gene[1]
                if person in have_trait:
                    probabilities2.append(PROBS["trait"][2][True]*tempprob)   
                else:
                    probabilities2.append(PROBS["trait"][2][False]*tempprob)   
                    
            else:
                tempprob = (1-probability_of_passing_gene[0])*(1-probability_of_passing_gene[1])
                if person in have_trait:
                    probabilities2.append(PROBS["trait"][0][True]*tempprob)   
                
                else:
                    probabilities2.append(PROBS["trait"][0][False]*tempprob)   
            probability_of_passing_gene = []          
    product = 1
    
    for p in probabilities2:
       
        product *= p
    return product


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    print(f'p is: {p}')
    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
            if person in have_trait:
                probabilities[person]["trait"][True] += p 
            else:
                probabilities[person]["trait"][False] += p 
        elif person in two_genes:
             probabilities[person]["gene"][2]  += p
             if person in have_trait:
                probabilities[person]["trait"][True] += p 
             else:
                probabilities[person]["trait"][False] += p 
        else:
            probabilities[person]["gene"][0]  += p
            if person in have_trait:
                probabilities[person]["trait"][True] += p 
            else:
                probabilities[person]["trait"][False] += p 


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        trait_val1 = probabilities[person]["trait"][True]
        trait_val2 = probabilities[person]["trait"][False]
        
        sum = trait_val1  + trait_val2        
        
        normalized_trait_val1 = trait_val1/sum
        normalized_trait_val2 = trait_val2/sum
        
        probabilities[person]["trait"][True] = normalized_trait_val1
        probabilities[person]["trait"][False] = normalized_trait_val2
        
        zero_val = probabilities[person]["gene"][0]
        one_val = probabilities[person]["gene"][1]
        two_val = probabilities[person]["gene"][2]
        sum2 = zero_val + one_val + two_val 
        
        normalized_zero_val = zero_val / sum2
        normalized_one_val = one_val / sum2
        normalized_two_val = two_val / sum2
        
        probabilities[person]["gene"][0] = normalized_zero_val 
        probabilities[person]["gene"][1] = normalized_one_val
        probabilities[person]["gene"][2] = normalized_two_val
        

if __name__ == "__main__":
    main()
