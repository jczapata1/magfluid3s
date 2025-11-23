module physics

    contains    
    
!-----------------------------------------------------------------------------------------------

        !! Temperature
        function T_(Ti, Tf, tt, t)

            ! Generate linearly time-dependent temperature.
            !
            ! Input:
            ! -  Ti (real*8): Initial Temperature         
            ! -  Tf (real*8): Final Temperature  
            ! -  tt (real*8): Total Time   
            ! -   t (real*8): Current Time
            !
            ! Output:  
            ! - T_ (real*8): Temperature     
            !
            ! Used by:
            ! - llg.run_MvsT
            ! - llg-t.run_MvsT

            real*8, intent(in) :: Ti, Tf, tt, t
            real*8             :: T_
            
            T_ = Ti + (Tf-Ti)/tt * t ! Linearly Time-Dependent Temperature
            
        end function T_         
    
!-----------------------------------------------------------------------------------------------

        !! Magnetic Field
        function H_(H0, f, t)

            ! Generate cosinusoidal time-dependent magnetic field in z-direction.
            !
            ! Input:
            ! -              H0 (real*8): Magnetic Field Amplitude         
            ! -               f (real*8): Magnetic Field Frecuency
            ! -               t (real*8): Current Time         
            !
            ! Output:  
            ! - H_ (real*8, array[3, 1]): Magnetic Field        
            !
            ! Used by:
            ! - llg.run_Microstates
            ! - llg.run_MvsH
            ! - llg.run_MvsT
            ! - llg-t.run_Microstates
            ! - llg-t.run_MvsH
            ! - llg-t.run_MvsT

            use constants, only : PI          
            real*8, intent(in) :: H0, f, t
            real*8             :: H_(0:2)
            
            H_ = [0.0d0, 0.0d0, H0*cos(2.0*PI*f*t)] ! Cosenoidal Time-Dependent Magnetic Field
            
        end function H_           
                 
!-----------------------------------------------------------------------------------------------

        !! Solvent Viscosity
        function ETA_(T0)

            ! Generate the solvent vicosity based on the Vogel–Fulcher–Tammann model.
            !
            ! Input:
            ! -   T0 (real*8): Temperature              
            !
            ! Output:  
            ! - ETA_ (real*8): Solvent Viscosity   
            !
            ! Used by:
            ! - llg-t.run_Microstates
            ! - llg-t.run_MvsH
            ! - llg-t.run_MvsT
         
            real*8, intent(in) :: T0
            real*8             :: TM, T_MAX, ETA_
            
            TM    = 273.15 ! Melting Temperature 
            T_MAX = 373.0  ! Maximum Temperature
            
            if (T0 < TM) then  
                ETA_ = 1.0d99                                               ! Solvent Viscosity  
            else if (T0 >= TM .and. T0 <= T_MAX) then
                ETA_ = 1.0d-3 * exp(-3.7188)* exp(578.9190/(T0 - 137.5460)) ! Solvent Viscosity                 
            else
                print *, "Invalid Temperature!. Use T0 < 373.0 K."
                stop 
            end if
                      
        end function ETA_
        
!-----------------------------------------------------------------------------------------------

        !! Drag Coefficients
        function Z_(N, Op, eta)

            ! Generate a configuration of drag coefficients.
            !
            ! Input:
            ! -              N (integer): Number of Particles         
            ! - Op (real*8, array[N, 1]): Particle Volumes List
            ! -             eta (real*8): Solvent Viscosity                        
            !
            ! Output:  
            ! -    Z_ (real*8, array[N]): Drag Coefficients List   
            !
            ! Used by:
            ! - llg-t.run_Microstates
            ! - llg-t.run_MvsH
            ! - llg-t.run_MvsT

            integer, intent(in) :: N
            real*8, intent(in)  :: Op(0:N-1), eta
            real*8              :: Z_(0:N-1)
            integer             :: i
        
#ifdef THREADS
    call omp_set_num_threads(THREADS)
#endif
           
            !$omp parallel do private(i) shared(Op, eta, Z_)
            do i = 0, N-1
                Z_(i) = 6.0 * eta * Op(i) ! Drag Coefficient
            end do
            !$omp end parallel do

        end function Z_
    
!-----------------------------------------------------------------------------------------------

        !! Thermal Field Standard Deviations
        function SH_(N, Mu, T0, alp, dt)

            ! Generate a configuration of thermal field standard deviations.
            !
            ! Input:
            ! -               N (integer): Number of Particles         
            ! -  Mu (real*8, array[N, 1]): Magnetic Moments (Magnitude) List
            ! -               T0 (real*8): Temperature       
            ! -              alp (real*8): Damping Parameter               
            ! -               dt (real*8): Integration Time                          
            !
            ! Output:  
            ! - SH_ (real*8, array[N, 1]): Thermal Field Standard Deviations List    
            !
            ! Used by:
            ! - llg.run_Microstates
            ! - llg.run_MvsH
            ! - llg.run_MvsT
            ! - llg-t.run_Microstates
            ! - llg-t.run_MvsH
            ! - llg-t.run_MvsT

            use constants, only  : KB, MU0, G
            integer, intent(in) :: N
            real*8, intent(in)  :: Mu(0:N-1), T0, alp, dt
            real*8              :: DH, SH_(0:N-1)
            integer             :: i
        
#ifdef THREADS
    call omp_set_num_threads(THREADS)
#endif
            
            !$omp parallel do private(i, DH) shared(Mu, T0, alp, dt, SH_)
            do i = 0, N-1
                DH     = ((KB*T0)/(MU0*Mu(i)*G)) * (alp/(1.0+alp**2)) ! Diffusion Coefficient
                SH_(i) = sqrt(2.0*DH*dt)                              ! Standard Deviation
            end do
            !$omp end parallel do

        end function SH_
        
!-----------------------------------------------------------------------------------------------

        !! Thermal Torque Standard Deviations
        function S0_(N, Z, T0, dt)

            ! Generate a configuration of thermal torque standard deviations.
            !
            ! Input:
            ! -               N (integer): Number of Particles         
            ! -   Z (real*8, array[N, 1]): Drag Coefficients List
            ! -               T0 (real*8): Temperature        
            ! -               dt (real*8): Integration Time             
            !
            ! Output:  
            ! - S0_ (real*8, array[N, 1]): Thermal Torque Standard Deviations List        
            !
            ! Used by:
            ! - llg-t.run_Microstates
            ! - llg-t.run_MvsH
            ! - llg-t.run_MvsT

            use constants, only  : KB          
            integer, intent(in) :: N
            real*8, intent(in)  :: Z(0:N-1), T0, dt
            real*8              :: D0, S0_(0:N-1)
            integer             :: i
        
#ifdef THREADS
    call omp_set_num_threads(THREADS)
#endif
             
            !$omp parallel do private(i, D0) shared(Z, T0, dt, S0_)
            do i = 0, N-1
                D0     = KB*T0*Z(i)      ! Diffusion Coefficient
                S0_(i) = sqrt(2.0*D0*dt) ! Standard Deviation
            end do
            !$omp end parallel do

        end function S0_
                              
!-----------------------------------------------------------------------------------------------

end module physics