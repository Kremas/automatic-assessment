#include "CUnit/CUnit.h"
#include "CUnit/Basic.h"

// INCLURE LE HEADER
#include "calc.h"

#include <stdio.h>

// required : libcunit1 libcunit1-doc libcunit1-dev
// gcc -Wall -c calc.c
// gcc -Wall -o calc_test calc_test.c calc.o -lcunit
// ./calc_test


/* Test fonctions init de suite et cleanup */

int init_suite(void) { return 0; }
int clean_suite(void) { return 0; }

/* Fonctions de test */

void test_case_sample(void)
{
    CU_ASSERT(CU_TRUE);
    CU_ASSERT_NOT_EQUAL(2, -1);
    CU_ASSERT_STRING_EQUAL("string #1", "string #1");
    CU_ASSERT_STRING_NOT_EQUAL("string #1", "string #2");

    CU_ASSERT(CU_FALSE);
    CU_ASSERT_EQUAL(2, 3);
    CU_ASSERT_STRING_NOT_EQUAL("string #1", "string #1");
    CU_ASSERT_STRING_EQUAL("string #1", "string #2");
}

void add_test(void) {
    CU_ASSERT_EQUAL( add(1,2), 3);
    CU_ASSERT_EQUAL( add(-5,1), -4);
}

void sub_test(void) {
    CU_ASSERT_EQUAL( sub(2,2), 0);
    CU_ASSERT_EQUAL( sub(0,0), 0);
    CU_ASSERT_EQUAL( sub(-1,-1), 0);
}

void mul_test(void) {
    CU_ASSERT_EQUAL( mul(-1,-5), 5);
    CU_ASSERT_EQUAL( mul(2,4), 8);
}

void div_test(void) {
    CU_ASSERT_EQUAL( div(5,0), 0);
    CU_ASSERT_EQUAL( div(7,2), 3.5);
    CU_ASSERT_EQUAL( div(4,2), 2);
}

void max_test(void) {
    CU_ASSERT_EQUAL( max(-1,-2), -1);
    CU_ASSERT_EQUAL( max(3,5), 5);
}

/* main */

int main (int argc, char **argv) {

    CU_pSuite pSuite = NULL;

    /* Initialisation du registre de CUnit */
    if ( CUE_SUCCESS != CU_initialize_registry() )
        return CU_get_error();

    /* Ajout de l'ensemble de tests au registre */
    pSuite = CU_add_suite( "calc_test_suite", init_suite, clean_suite );
    if ( NULL == pSuite ) {
        // Si probleme : Nettoyage du registre et return
        CU_cleanup_registry();
        return CU_get_error();
    }

    /* Ajout des tests a l'ensemble de tests */
    if ( (NULL == CU_add_test(pSuite, "add_test", add_test)) ||
         (NULL == CU_add_test(pSuite, "sub_test", sub_test)) ||
         (NULL == CU_add_test(pSuite, "mul_test", mul_test)) ||
         (NULL == CU_add_test(pSuite, "div_test", div_test)) ||
         (NULL == CU_add_test(pSuite, "max_test", max_test))
       )
    {
        // Si probleme : Nettoyage du registre et return
        CU_cleanup_registry();
        return CU_get_error();
    }

    /* Execution des tests avec l'interface basique */
    CU_basic_set_mode(CU_BRM_VERBOSE);
    CU_basic_run_tests();
    CU_basic_show_failures(CU_get_failure_list());

    /* Nettoyage du registre et return */
    CU_cleanup_registry();
    return CU_get_error();
} // Fin du main
