module math 

    contains
           
!---------------------------------------------------------------------------        

        !! Random Number - Normal Distribution
        function r_normal(sigma)

            ! Generate random number with normal distribution.
            !
            ! Input:      
            ! -    sigma (real*8): Standard Deviation
            !
            ! Output:  
            ! - r_normal (real*8): Random Number  
            !
            ! Used by:
            ! - solvers.libs.math.rv_normal
            !
            ! Last Updated: 
            ! - 16/08/2026

            use constants, only : PI
            real*8, intent(in) :: sigma
            real*8             :: r_normal
            real*8             :: u, v

            call random_number(u)
            call random_number(v)
            u        = max(u, tiny(1.0d0))
            r_normal = sigma * sqrt(-2.0d0*log(u)) * cos(2.0d0*PI*v)

        end function r_normal
        
!---------------------------------------------------------------------------  
        
        !! Random Vector - Normal Distribution
        function rv_normal(sigma)

            ! Generate random 3D-vector with normal distribution.
            !
            ! Input:          
            ! -                    sigma (real*8): Standard Deviation
            !
            ! Output:  
            ! - r_vector ((real*8, ), array[3, ]): Random Vector    
            !
            ! Used by:
            ! - solvers.llg.integration.stratonovich_heun
            ! - solvers.llg-t.integration.stratonovich_heun
            !
            ! Last Updated: 
            ! - 16/08/2026

            implicit none
            real*8, intent(in) :: sigma
            real*8             :: rv_normal(0:2)
            
            rv_normal = [r_normal(sigma), r_normal(sigma), r_normal(sigma)]

        end function rv_normal
        
!---------------------------------------------------------------------------

        !! Dot Product
        pure function dot_prod(U, V)

            ! Calculate the dot product of two 3D-vectors.
            !
            ! Input:
            !  -     U ((real*8, ), array[3, ]): Vector 1
            !  -     V ((real*8, ), array[3, ]): Vector 2
            !
            ! Output:
            ! -              dot_prod (real*8): Dot Product     
            !
            ! Used by:
            ! - solvers.llg.integration.stratonovich_heun
            ! - solvers.llg-t.integration.stratonovich_heun
            !
            ! Last Updated: 
            ! - 16/08/2026

            implicit none
            real*8, intent(in) :: U(0:2), V(0:2)
            real*8             :: dot_prod

            dot_prod = U(0)*V(0) + U(1)*V(1) + U(2)*V(2)

        end function dot_prod
        
!---------------------------------------------------------------------------        
        
        !! Cross Product
        pure function cross_prod(U, V)

            ! Calculate the cross product of two 3D-vectors.
            !
            ! Input:
            !  -         U ((real*8, ), array[3, ]): Vector 1
            !  -         V ((real*8, ), array[3, ]): Vector 2
            !
            ! Output:
            ! - cross_prod ((real*8, ), array[3, ]): Cross Product    
            !
            ! Used by:
            ! - solvers.llg.integration.stratonovich_heun
            ! - solvers.llg-t.integration.stratonovich_heun
            !
            ! Last Updated: 
            ! - 16/08/2026

            implicit none
            real*8, intent(in) :: U(0:2), V(0:2)
            real*8             :: cross_prod(0:2)

            cross_prod(0) = U(1)*V(2) - U(2)*V(1) 
            cross_prod(1) = U(2)*V(0) - U(0)*V(2) 
            cross_prod(2) = U(0)*V(1) - U(1)*V(0)        

        end function cross_prod       
        
!---------------------------------------------------------------------------

end module math